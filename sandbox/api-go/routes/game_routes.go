package routes

import (
	"KegwatchApi/common_db"
	"KegwatchApi/common_log"
	"KegwatchApi/constants"
	"KegwatchApi/types"
	"encoding/json"
	"fmt"
	"net/http"
)

const (
	gamesPathSegment = "/games"
)

var GameRoutes = Routes{
	Route{
		"GetGames",
		constants.GET,
		gamesPathSegment,
		GetGames,
	},
	Route{
		"CreateGame",
		constants.POST,
		gamesPathSegment,
		CreateGame,
	},
	Route{
		"UpdateGame",
		constants.PUT,
		gamesPathSegment + "/edit",
		UpdateGame,
	},
}

// GetGames godoc
// @Summary      Get all games
// @Description  Get all games with single GET and no params
// @Tags         games
// @Accept       json
// @Produce      json
// @Success      200  {object}  []types.Game
// @Failure      404
// @Failure      500  {object}  string
// @Router       /games [get]
func GetGames(w http.ResponseWriter, r *http.Request) {
	fmt.Println("IN GETGAMES")

	common_db.VerifyDbConn(r)
	gameBytes, err := common_db.GetAllGames()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	_, writeErr := w.Write(gameBytes)
	common_log.FancyHandleError(writeErr)
}

// CreateGame godoc
// @Summary      Create game from provided JSON
// @Description  Insert single Game with POST body and no URL params
// @Tags         games
// @Accept       json
// @Produce      plain
// @Param				game body types.Game true "Game to be recorded"
// @Success      200
// @Failure      400  {object}  string
// @Failure      404
// @Failure      500  {object}  string
// @Router       /games [POST]
func CreateGame(w http.ResponseWriter, r *http.Request) {
	// We're looking for a post - the pre-flight request is stupid, short-circuit now lol
	if r.Method == http.MethodOptions {
		return
	}

	common_db.VerifyDbConn(r)

	// Body -> Game struct conversion
	var g types.Game
	err := json.NewDecoder(r.Body).Decode(&g)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	afterInsertErr := common_db.InsertGame(g)
	if afterInsertErr != nil {
		http.Error(w, afterInsertErr.Error(), http.StatusInternalServerError)
		return
	}

	// Barf
	w.WriteHeader(http.StatusOK)
}

// Update, as a PUT request function, will just replace the existing game
//
//	which should provide a little better extension of functionality in the future

// UpdateGame godoc
// @Summary      Replace existing game with provided JSON
// @Description  Overwrite single Game with PUT body and no URL params
// @Tags         games
// @Accept       json
// @Produce      plain
// @Param				game body types.Game true "Game to be replaced"
// @Success      200
// @Failure      400  {object}  string
// @Failure      404
// @Failure      500  {object}  string
// @Router       /games/edit [PUT]
func UpdateGame(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodOptions {
		return
	}

	var g types.Game
	err := json.NewDecoder(r.Body).Decode(&g)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	common_db.VerifyDbConn(r)
	err = common_db.UpdateGame(g)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
}
