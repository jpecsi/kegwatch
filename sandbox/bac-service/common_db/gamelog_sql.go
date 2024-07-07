package common_db

import (
	"KwGameSvc/types"
	"fmt"
)

func GetDrinksInGame(userId string, game types.Game) ([]types.Drink, error) {
	drinks := make([]types.Drink, 0)

	// Hit the database to see what drinks the user has had as a part of the game
	query := fmt.Sprintf(`SELECT bev_abv, amount_consumed, time, consumer
		FROM game_log WHERE game = '%+v' and consumer = '%+v'`, game.Id, userId)
	rows, err := GetDb().Query(query)
	if err != nil {
		return drinks, err
	}

	// Deserialize MySQL rows to the array of drinks
	SqlRowsToDrinks(rows, &drinks)

	return drinks, nil
}
