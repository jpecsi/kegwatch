package common_db

import (
	"KwGameSvc/types"
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

func GetPlayersOfGame(gameId string) ([]types.Player, error) {
	players := make([]types.Player, 0)

	rows, err := GetDb().Query(fmt.Sprintf(`SELECT c.id, c.body_cat, c.grams, c.is_female, t.team
		FROM consumers c
		INNER JOIN teams t 
		ON t.consumer = c.id 
		WHERE t.game='%+v'`, gameId))
	if err != nil {
		return players, err
	}

	player := types.NewPlayer()
	for rows.Next() {
		err := rows.Scan(&player.Id, &player.BodyCat, &player.Grams, &player.IsFemale, &player.Team)
		if err != nil {
			return players, err
		}

		players = append(players, player)

		// Ensure no carry-over of optional fields not overwritten (grams)
		player = types.NewPlayer()
	}

	playersJs, _ := json.Marshal(players)
	fmt.Printf("Players of game: %+v", string(playersJs))

	return players, nil
}
