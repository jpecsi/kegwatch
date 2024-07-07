package routes

import (
	"KegwatchApi/common_db"
	"KegwatchApi/constants"
	"KegwatchApi/types"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
)

const (
	beerPathSegment = "/beer"
)

var BeerRoutes = Routes{
	Route{
		"AddBeerRecord",
		constants.POST,
		beerPathSegment,
		AddBeerRecord,
	},
	Route{
		"AttributeBeerRecord",
		constants.PUT,
		beerPathSegment + "/{userId}",
		AttributeBeerRecord,
	},
}

// AddBeerRecord godoc
// @Summary     Create single record of pour from provided JSON
// @Description  Insert single beer to beer_log with POST body and no URL params
// @Tags         beer
// @Accept       json
// @Produce      plain
// @Param     	beer body types.Beer true "Beer to be recorded"
// @Success      200
// @Failure      400  {object}  string
// @Failure      404
// @Failure      500  {object}  string
// @Router       /beer [POST]
func AddBeerRecord(w http.ResponseWriter, r *http.Request) {
	// We're looking for a post - the pre-flight request is stupid, short-circuit now lol
	if r.Method == http.MethodOptions {
		return
	}

	fmt.Println("Adding beer to the beer_log")

	common_db.VerifyDbConn(r)

	// Body -> User struct conversion
	var b types.Beer
	err := json.NewDecoder(r.Body).Decode(&b)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Get info from keg if the pour data is lacking
	if len(b.BeerId) == 0 || len(b.BeerName) == 0 {
		k := common_db.KegInTap(b.TapId)

		// Be defensive about the ID provided:
		if k.Id == nil || len(*k.Id) < 1 {
			http.Error(w, "You.. just poured from a tap that doesn't have a keg in it.. we're just gonna.. throw that away", http.StatusBadRequest)
			return
		}

		b.BeerId = *k.Id
		if len(k.Name) > 0 {
			b.BeerName = k.Name
		}
	}

	afterInsertErr := common_db.InsertPour(b)
	if afterInsertErr != nil {
		http.Error(w, afterInsertErr.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
}

// AttributeBeerRecord godoc
// @Summary     Create single record of pour from provided JSON
// @Description  Update single (last poured) beer to beer_log with PUT request (no body) and the consumer as a URL parameter
// @Tags         beer
// @Accept       json
// @Produce      plain
// @Param     	user path string true "User to attribute the last pour to"
// @Success      200
// @Failure      400  {object}  string
// @Failure      404
// @Failure      500  {object}  string
// @Router       /beer/{user} [PUT]
func AttributeBeerRecord(w http.ResponseWriter, r *http.Request) {
	// We're looking for a post - the pre-flight request is stupid, short-circuit now lol
	if r.Method == http.MethodOptions {
		return
	}

	fmt.Println("Adding beer to the beer_log")

	// Snatch the url param
	vars := mux.Vars(r)
	user := vars["userId"]

	common_db.VerifyDbConn(r)

	b, err := common_db.AttributePour(user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	response := fmt.Sprintf("Attributed pour: %+voz of %+v was made by %+v at %+v", b.OzPoured, b.BeerName, user, b.PourTime)
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(response))
}
