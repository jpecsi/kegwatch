package routes

import (
	"KegwatchApi/common_db"
	"KegwatchApi/constants"
	"KegwatchApi/types"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
)

const (
	teamsPathSegment = "/teams"
)

var TeamRoutes = Routes{
	Route{
		"GetTeams",
		constants.GET,
		teamsPathSegment,
		GetTeams,
	},
	Route{
		"CreateTeam",
		constants.POST,
		teamsPathSegment,
		CreateTeam,
	},
}

// GetTeams godoc
// @Summary      Get all teams
// @Description  Gets all teams stored in DB, represented in JSON format
// @Tags         teams
// @Accept       json
// @Produce      json
// @Success      200  {array}  types.TeamAffiliation
// @Failure      404
// @Failure      500  {object}  string
// @Router       /teams [GET]
func GetTeams(w http.ResponseWriter, r *http.Request) {
	fmt.Println("IN GETTEAMS")

	common_db.VerifyDbConn(r)
	teamBytes, err := common_db.GetAllTeams()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write(teamBytes)
}

// CreateTeam godoc
// @Summary     Create a team
// @Description  	Creates a single team as indicated by the JSON provided in the POST request body
// @Tags         	teams
// @Accept       json
// @Produce      text/plain
// @Param				team body types.TeamAffiliation true "Team to be recorded"
// @Success      200
// @Failure      400  {object}  string
// @Failure      404
// @Router       /teams [POST]
func CreateTeam(w http.ResponseWriter, r *http.Request) {
	fmt.Println("IN CREATETEAM")

	// We're looking for a post - the pre-flight request is stupid, short-circuit now lol
	if r.Method == http.MethodOptions {
		return
	}

	common_db.VerifyDbConn(r)

	// Body -> Team struct conversion
	var t types.TeamAffiliation
	err := json.NewDecoder(r.Body).Decode(&t)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	afterInsertErr := common_db.InsertTeam(t)
	if afterInsertErr == nil {
		w.WriteHeader(http.StatusOK)
		return
	}

	// Barf
	w.WriteHeader(http.StatusInternalServerError)
	log.Fatalln(afterInsertErr.Error())
}
