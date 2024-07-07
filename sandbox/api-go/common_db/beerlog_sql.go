package common_db

import (
	"KegwatchApi/common_log"
	"KegwatchApi/types"
	"errors"
	"fmt"
)

func GetTotalPouredByUser(uid string) (int, error) {
	query := fmt.Sprintf("SELECT SUM(oz_poured) from beer_log where consumer = '%+v'", uid)
	rows, err := GetDb().Query(query)
	if err != nil {
		newErrTxt := fmt.Sprintf("Failed to get total poured using query %+v: ", query)
		return 0, errors.New(newErrTxt + err.Error())
	}

	total := float64(0.0)
	for rows.Next() {
		err := rows.Scan(&total)
		if err != nil {
			return 0, errors.New("Failed to load total SUM(oz_poured) into float64: " + err.Error())
		}
	}

	return int(total), nil
}

// Returns beer type poured most frequently by user
func GetUserFavorite(uid string) (string, error) {
	favoriteBeerQuery := fmt.Sprintf(`SELECT 
	beer_name,
	COUNT(beer_name) AS 'value_occurrence'
	FROM beer_log 
	WHERE consumer = '%+v'
	GROUP BY beer_name

	ORDER BY 'value_occurrence' DESC
	LIMIT 1`, uid)

	rows, err := GetDb().Query(favoriteBeerQuery)
	if err != nil {
		return "", err
	}

	var beerName string
	var valOccurrence int
	var scanErr error

	for rows.Next() {
		scanErr = rows.Scan(&beerName, &valOccurrence)
	}

	if scanErr != nil {
		scanErr = errors.New("Error in GetUserFavorite: " + scanErr.Error())
	}

	return beerName, scanErr
}

// Adds a user's pour to the beer_log table AND calls UpdateBeerRemaining for the keg
func InsertPour(b types.Beer) error {
	// Actual DB query
	insertQuery := fmt.Sprintf("INSERT INTO beer_log(time, tap_id, beer_id, beer_name, consumer, oz_poured) VALUES ('%+v', %d, '%+v', '%+v', '%+v', %f)", b.PourTime, b.TapId, b.BeerId, b.BeerName, b.Consumer, b.OzPoured)
	res, err := GetDb().Exec(insertQuery)
	if err != nil {
		return err
	}

	kegUpdateErr := UpdateBeerRemaining(b.OzPoured, b.TapId)
	if kegUpdateErr != nil {
		return fmt.Errorf("failed to update beer remining in tap #%+v: %+v", b.TapId, kegUpdateErr)
	}

	// Ensure everything went ok
	_, afterInsertErr := res.LastInsertId()

	return afterInsertErr
}

// Adds a user's pour to the beer_log table AND calls UpdateBeerRemaining for the keg
func AttributePour(user string) (*types.Beer, error) {
	lastPourQuery := fmt.Sprintf("SELECT time, beer_name, oz_poured FROM beer_log WHERE consumer = 'Anonymous' ORDER BY time desc limit 1")
	rows, err := GetDb().Query(lastPourQuery)
	if err != nil {
		return nil, err
	}

	var b types.Beer
	var scanErr error
	for rows.Next() {
		scanErr = rows.Scan(&b.PourTime, &b.BeerName, &b.OzPoured)
		common_log.FancyHandleError(scanErr)

		if scanErr != nil {
			return nil, scanErr
		}
	}

	updateErr := UpdateConsumer(user, b.PourTime)
	common_log.FancyHandleError(updateErr)

	return &b, updateErr
}

func UpdateConsumer(user, time string) error {
	updateQuery := fmt.Sprintf(`UPDATE beer_log
		SET consumer = '%+v',		
		WHERE time = '%+v';`, user, time)
	res, err := GetDb().Exec(updateQuery)

	ra, _ := res.RowsAffected()
	fmt.Printf("Updated consumer to %+v on %+v record.\n", user, ra)

	return err
}
