package common_db

import (
	"KegwatchApi/types"
	"encoding/json"
	"fmt"
	"log"
)

func GetAllTeams() ([]byte, error) {
	rows, err := GetDb().Query("SELECT game, consumer, team from teams")
	if err != nil {
		return []byte{}, err
	}

	t := types.TeamAffiliation{}
	teams := make([]types.TeamAffiliation, 0)
	for rows.Next() {
		err := rows.Scan(&t.Game, &t.Consumer, &t.Team)
		if err != nil {
			return []byte{}, err
		}

		fmt.Printf("%+v\n", t)
		teams = append(teams, t)
	}

	teamBytes, marshErr := json.Marshal(teams)
	if marshErr != nil {
		log.Fatalln(marshErr)
	}

	return teamBytes, marshErr
}

func InsertTeam(g types.TeamAffiliation) error {
	// Actual DB insertion
	insertQuery := fmt.Sprintf("INSERT INTO teams(game, consumer, team) VALUES ('%+v', '%+v', '%+v')", g.Game, g.Consumer, g.Team)
	res, err := GetDb().Exec(insertQuery)
	if err != nil {
		return err
	}

	// Ensure everything went ok
	_, afterInsertErr := res.LastInsertId()

	return afterInsertErr
}
