package routes

import (
	"KegwatchApi/common_db"
	"KegwatchApi/constants"
	"KegwatchApi/types"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
)

const (
	usersPathSegment = "/users"
)

var UserRoutes = Routes{
	Route{
		"GetUserPass",
		constants.GET,
		"/pass/user/{userId}",
		GetUserPass,
	},
	Route{
		"GetUsers",
		constants.GET,
		usersPathSegment,
		GetUsers,
	},
	Route{
		"CreateUser",
		constants.POST,
		usersPathSegment,
		CreateUser,
	},
}

// GetUsers godoc
// @Summary      Get all users
// @Description  Get all users with single GET and no params
// @Tags         users
// @Accept       json
// @Produce      json
// @Success      200  {array}  types.User
// @Failure      404
// @Failure      500  {object}  string
// @Router       /users [GET]
func GetUsers(w http.ResponseWriter, r *http.Request) {
	logger.Debugln("In GetUsers")

	common_db.VerifyDbConn(r)
	userBytes, err := common_db.GetAllUsers()
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(err.Error()))

		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write(userBytes)
}

// GetUserPass godoc
// @Summary      Get single user pass
// @Description  Gets pass of user with provided ID, returns current BAC from downstream BAC service and other associated user info
// @Tags         users
// @Accept       json
// @Produce      json
// @Param	      id 		query string true "User ID"
// @Success      200  {object}  types.UserPass
// @Failure      404
// @Failure      500  {object}  string
// @Router       /pass/user/{userId} [GET]
func GetUserPass(w http.ResponseWriter, r *http.Request) {
	logger.Debugln("In GetUserPass")

	vars := mux.Vars(r)
	uid := vars["userId"]

	// To ensure we get this done as efficiently as possible:
	//   call now, populate when the return value is obtained,
	//   and work on the rest in the meantime
	bacChan := make(chan float32)

	// Begin request in goroutine
	go func(bacChan chan float32, uid string) {
		logger.Infoln("Fetching current bac")
		err := FetchCurrentBac(bacChan, uid)

		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)

			w.Write([]byte(fmt.Sprintf("error: %+v\n", err)))
			w.Write([]byte("failed to fetch BAC from bac-service: " + err.Error()))
		}
	}(bacChan, uid)

	// Scrape userId and correct HTML escapes
	sanitizeSpaces(&uid)
	common_db.VerifyDbConn(r)

	logger.Infoln("Getting UserPass values")
	up, err := GetUserPassValues(uid)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("failed to complete UserPass oz/fav-beer DB calls: " + err.Error()))

		return
	}

	// Receive the current BAC value requested from
	//   the bac-service in a separate goroutine
	logger.Infoln("Awaiting bac from bacChan")
	up.Bac = <-bacChan

	logger.Infof("Got bac from bacChan: %+v", up.Bac)
	upBytes, marshErr := json.Marshal(up)
	if marshErr != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("failed to marshal UserPass: " + marshErr.Error()))

		return
	}

	logger.Infof("All good; returning %+v", string(upBytes))
	w.WriteHeader(http.StatusOK)
	w.Write(upBytes)
}

// CreateUser godoc
// @Summary      Create user from provided JSON
// @Description  Insert single User with POST body and no URL params
// @Tags         users
// @Accept       json
// @Produce      plain
// @Param				user body types.User true "User to be recorded"
// @Success      200
// @Failure      400  {object}  string
// @Failure      404
// @Failure      500  {object}  string
// @Router       /users [POST]
func CreateUser(w http.ResponseWriter, r *http.Request) {
	fmt.Println("IN CREATEUSER")

	// We're looking for a post - the pre-flight request is stupid, short-circuit now lol
	if r.Method == http.MethodOptions {
		return
	}

	common_db.VerifyDbConn(r)

	// Body -> User struct conversion
	var u types.User
	err := json.NewDecoder(r.Body).Decode(&u)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	afterInsertErr := common_db.InsertUser(u)
	if afterInsertErr != nil {
		fmtedErr := fmt.Sprintf("Failed to insert user: %+v\n", afterInsertErr)
		logger.Errorln(fmtedErr)
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(fmtedErr))

		return
	}

	// Barf
	w.WriteHeader(http.StatusOK)
}

/* Helper Functions */

func sanitizeSpaces(uid *string) {
	// Correct for HTML escaped spaces
	*uid = strings.Replace(*uid, "%20", " ", -1)
	*uid = strings.Replace(*uid, "+", " ", -1)

	// Remove any leading/trailing spaces
	*uid = strings.TrimSpace(*uid)
}

func FetchCurrentBac(bacChan chan<- float32, uid string) error {
	curBacUrl := "http://game-kw:8082/bac/user/" + uid
	logger.Infof("Calling %+v", curBacUrl)

	res, err := http.Get(curBacUrl)
	if err != nil {
		return err
	}

	logger.Infoln("Got response, reading body")
	defer res.Body.Close()
	var bacJson []byte
	bacJson, readErr := io.ReadAll(res.Body)
	if readErr != nil {
		return readErr
	}

	logger.Infoln("Read body; unmarshaling..")
	var bacReading types.BacReading
	umarshErr := json.Unmarshal(bacJson, &bacReading)
	if umarshErr != nil {
		return umarshErr
	}

	bacChan <- bacReading.BacPct
	return nil
}

func GetUserPassValues(uid string) (types.UserPass, error) {
	var err error
	var up types.UserPass
	up.Name = uid

	up.Oz, err = common_db.GetTotalPouredByUser(uid)
	if err != nil {
		return types.UserPass{}, err
	}

	up.Beer, err = common_db.GetUserFavorite(uid)
	return up, err
}
