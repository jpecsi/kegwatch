package common_db

import (
	"KwGameSvc/types"
	"fmt"
)

func InsertBac(bac float32, player types.Player, game types.Game, updateTime string) error {
	if bac == 0.0 {
		return nil
	}

	fmt.Printf("\n\nInserting BAC %f for %+v\n\n", bac, player.Id)

	insertQuery := fmt.Sprintf(`INSERT INTO bac_log 
		(game, consumer, time, bac, team) VALUES
		('%+v', '%+v', '%+v', %.3f, '%+v')`, game.Id, player.Id, updateTime, bac, player.Team)
	_, err := GetDb().Query(insertQuery)
	return err

}
