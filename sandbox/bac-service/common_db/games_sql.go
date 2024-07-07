package common_db

import (
	"KwGameSvc/types"
	"encoding/json"
	"fmt"
	"log"
)

func GetAllGames() ([]byte, error) {
	rows, err := GetDb().Query("SELECT id, description, date, status from games")
	if err != nil {
		return []byte{}, err
	}

	g := types.Game{}
	games := make([]types.Game, 0)
	for rows.Next() {
		err := rows.Scan(&g.Id, &g.Description, &g.Date, &g.Status)
		if err != nil {
			return []byte{}, err
		}

		fmt.Printf("%+v\n", g)
		games = append(games, g)
	}

	gameBytes, marshErr := json.Marshal(games)
	if marshErr != nil {
		log.Fatalln(marshErr)
	}

	return gameBytes, marshErr
}

func GetActiveGames() ([]types.Game, error) {
	rows, err := GetDb().Query("SELECT id, description, date, status from games where status=1")
	if err != nil {
		return []types.Game{}, err
	}

	g := types.Game{}
	games := make([]types.Game, 0)
	for rows.Next() {
		err := rows.Scan(&g.Id, &g.Description, &g.Date, &g.Status)
		if err != nil {
			return []types.Game{}, err
		}

		fmt.Printf("%+v\n", g)
		games = append(games, g)
	}

	return games, err
}
