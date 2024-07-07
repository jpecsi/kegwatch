package common_db

import (
	"KegwatchApi/types"
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

func GetGameById() {

}

func InsertGame(g types.Game) error {
	// Actual DB insertion
	insertQuery := fmt.Sprintf("INSERT INTO games(id, description, date, status) VALUES ('%+v', '%+v', '%+v', %+v)", g.Id, g.Description, g.Date, g.Status)
	res, err := GetDb().Exec(insertQuery)
	if err != nil {
		return err
	}

	// Ensure everything went ok
	_, afterInsertErr := res.LastInsertId()

	return afterInsertErr
}

func UpdateGame(g types.Game) error {
	// Test
	gameToUpdate, marshErr := json.Marshal(g)
	if marshErr != nil {
		fmt.Printf("failed to marshal game received in UpdateGame: %+v", marshErr)
		return marshErr
	}

	fmt.Printf("Received game to update in UpdateGame: %+v", gameToUpdate)

	updateQuery := fmt.Sprintf(`UPDATE games
		SET description = '%+v',
			date = '%+v',
			status = '%+v'
		WHERE id = '%+v';`, g.Description, g.Date, g.Status, g.Id)
	res, err := GetDb().Exec(updateQuery)

	ra, errRows := res.RowsAffected()
	fmt.Printf("%+v rows affected; %+v", ra, errRows)

	return err
}
