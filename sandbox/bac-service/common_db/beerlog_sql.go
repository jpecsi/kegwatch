package common_db

import (
	"KwGameSvc/constants"
	"KwGameSvc/types"
	"database/sql"
	"encoding/json"
	"fmt"
	"time"
)

// Returns drinks logged to beer_log
func GetDrinksWithImpact(userId string) ([]types.Drink, error) {
	twelveHrAgo := time.Now().Add(time.Duration(-12 * time.Hour))
	twelveHrFmt := twelveHrAgo.Format(constants.TIME_FMT)

	drinks := make([]types.Drink, 0)

	logger.Infof("12h ago: %+v", twelveHrFmt)

	// Hit the database to see what drinks the user has had as a part of the game
	query := fmt.Sprintf(`SELECT 
		k.abv, 
		b.oz_poured, 
		b.time,
		b.consumer
		FROM beer_log b
		INNER JOIN keg_log k ON b.beer_id = k.id
		WHERE b.time > date('%+v') and b.consumer = '%+v'`, twelveHrFmt, userId)

	rows, err := GetDb().Query(query)
	if err != nil {
		return drinks, err
	}

	// Deserialize MySQL rows to the array of drinks
	err = SqlRowsToDrinks(rows, &drinks)
	logger.Infof("Drinks %+v has had since %+v: %d", userId, twelveHrFmt, len(drinks))

	return drinks, err
}

func SqlRowsToDrinks(rows *sql.Rows, drinks *[]types.Drink) error {
	// Convert DB results to Drink structs
	for rows.Next() {
		drink := types.Drink{}
		rTime := RawTime{}

		err := rows.Scan(&drink.Abv, &drink.Oz, &rTime, &drink.User)
		if err != nil {
			return err
		}

		// Use the RawTime struct to properly
		//   unmarshal MySQL's drink timestamp
		drink.Time = rTime.Time()
		jsb, err := json.Marshal(drink)
		if err == nil {
			fmt.Println(string(jsb))
		}

		*drinks = append(*drinks, drink)
	}

	return nil
}
