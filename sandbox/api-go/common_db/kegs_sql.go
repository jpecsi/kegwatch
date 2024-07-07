package common_db

import (
	"KegwatchApi/common_log"
	"KegwatchApi/constants"
	"KegwatchApi/types"
	"encoding/json"
	"fmt"
	"time"

	"github.com/sirupsen/logrus"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

const (
	getAllKegs = "SELECT * from keg_log"
)

// SELECT Queries ============

func GetAllKegs() ([]byte, error) {
	kegBytes, err := fetchKegsWithQuery(getAllKegs)
	return kegBytes, err
}

func GetActiveKegs() ([]byte, error) {
	return fetchKegsWithQuery(fmt.Sprintf("%+v WHERE status = '%+v'", getAllKegs, constants.Active))
}

func GetActiveKegByTapNo(tapNo int) (types.Keg, error) {
	var kegs []types.Keg
	kegBytes, fetchErr := fetchKegsWithQuery(fmt.Sprintf("%+v WHERE status = '%+v' AND tap = '%+v'", getAllKegs, constants.Active, tapNo))
	common_log.FancyHandleError(fetchErr)

	err := json.Unmarshal(kegBytes, &kegs)
	common_log.FancyHandleError(err)

	var retErr error
	if len(kegs) != 1 {
		retErr = fmt.Errorf("found incorrect number of active kegs on tap %+v: %+v", tapNo, len(kegs))
		return types.Keg{}, retErr
	}

	return kegs[0], nil
}

// ===========================

// Assumption: All oz are remaining on insert
func InsertKeg(k types.Keg) (string, error) {
	if k.Id == nil || len(*k.Id) < 1 {
		newOid := primitive.NewObjectID().Hex()
		logrus.Infof("")
		k.Id = &newOid
	}

	if kj, miErr := json.MarshalIndent(k, "", "  "); miErr != nil {
		common_log.FancyHandleError(miErr)
	} else {
		fmt.Printf("Inserting Keg %+v\n", string(kj))
	}

	// Actual DB insertion
	res, err := GetDb().Exec(buildKegInsertQuery(k))
	if err != nil {
		common_log.FancyHandleError(err)
		return "", err
	}

	// Ensure everything went ok
	_, afterInsertErr := res.LastInsertId()

	return *k.Id, afterInsertErr
}

func buildKegInsertQuery(k types.Keg) string {
	if k.DaysToConsume == nil {
		return fmt.Sprintf(
			"INSERT INTO keg_log( "+
				"id, name, tap, abv, capacity, remaining, date_tapped, status "+
				") VALUES ("+
				"'%+v', '%+v', '%d', '%.1f', '%d', '%.1f', '%+v', '%d')",
			*k.Id, k.Name, k.Tap, k.Abv, k.Capacity, *k.Remaining,
			*k.DateTapped, k.Status)
	}

	return fmt.Sprintf(
		"INSERT INTO keg_log( "+
			"id, name, tap, abv, capacity, remaining, date_tapped, days_to_consume, status "+
			") VALUES ("+
			"'%+v', '%+v', '%d', '%.1f', '%d', '%.1f', '%+v', '%+v', '%d')",
		*k.Id, k.Name, k.Tap, k.Abv, k.Capacity, *k.Remaining,
		*k.DateTapped, *k.DaysToConsume, k.Status)
}

// Reduce keg's remaining value by the oz from pour
func UpdateBeerRemaining(ozPoured float32, tapNo int) error {
	initialOzQuery := fmt.Sprintf(`SELECT remaining, id, date_tapped from keg_log	
	WHERE status = '%+v'
	AND tap = '%+v'`, constants.Active, tapNo)

	// Get oz remaining, as well as other potentially relevant fields from keg_log
	rows, err := GetDb().Query(initialOzQuery)
	if err != nil {
		return fmt.Errorf("failed to query for initial amount remaining from keg in tap #%+v: %+v", tapNo, err)
	}

	// Query result variables
	var ozRemaining float32
	var id string
	var dateTapped string

	matched := 0
	for rows.Next() {
		// Iteratable rows doesn't have len - check manually:
		matched++
		if matched > 1 {
			return fmt.Errorf("somehow received more than one keg when querying active kegs in tap #%+v -- this can't happen", tapNo)
		}

		// Scan ozRemaining (id and dateTapped also selected in case we need to kick)
		if err := rows.Scan(&ozRemaining, &id, &dateTapped); err != nil {
			return fmt.Errorf("failed to scan the remaining, id, and/or date tapped values: %+v", err)
		}
	}

	newRemaining := ozRemaining - ozPoured
	updateQuery := fmt.Sprintf(`UPDATE keg_log
		SET remaining = '%+v'
		WHERE id = '%+v'`, newRemaining, id)

	res, err := GetDb().Exec(updateQuery)
	ra, _ := res.RowsAffected()
	fmt.Printf("%+v rows affected in UpdateBeerRemaining", ra)

	return err
}

// Ensure the tap of a keg that is being activated is free (nil return value is good)
func KegInTap(tapNo int) *types.Keg {
	initialOzQuery := fmt.Sprintf(`SELECT remaining, id, name, capacity, abv, remaining from keg_log
		WHERE status = '%+v'
		AND tap = '%+v'`, constants.Active, tapNo)

	rows, err := GetDb().Query(initialOzQuery)
	if err != nil {
		fmt.Printf("Error occurred while querying for beer in tap does this mean there isn't one? I'm assuming it does. %+v", err)
		return nil
	}

	// Query result variable
	var k types.Keg
	k.Tap = tapNo
	kegFound := false

	for rows.Next() {
		if err := rows.Scan(&k.Remaining, &k.Id, &k.Name, &k.Capacity, &k.Abv, &k.Remaining); err != nil {
			fmt.Printf("failed to scan the remaining, id, and/or name values: %+v", err)
			continue
		}

		kegFound = true
	}

	if kegFound {
		return &k
	}

	return nil
}

// Kick the keg
func KickKeg(id string, dateTapped string) error {
	date, err := time.Parse(constants.DATE_FMT, dateTapped)
	if err != nil {
		return fmt.Errorf("failed to parse dateTapped as YYYY-MM-DD: %+v", err)
	}

	today := time.Now()
	diff := today.Sub(date)

	updateQuery := fmt.Sprintf(`UPDATE keg_log
		SET status = '%+v'
		days_to_consume = '%+v'
		date_kicked = '%+v'
		WHERE id ='%+v'
		`,
		constants.Inactive,               // Status
		int(diff.Hours()/24),             // Days to Consume
		today.Format(constants.DATE_FMT), // Date Kicked
		id,                               // ID
	)

	res, err := GetDb().Exec(updateQuery)
	ra, _ := res.RowsAffected()
	fmt.Printf("%+v rows affected in KickKeg", ra)

	return err
}

// Perform a SELECT query on the keg_log table
func fetchKegsWithQuery(query string) ([]byte, error) {
	rows, err := GetDb().Query(query)
	if err != nil {
		common_log.FancyHandleError(err)
		return []byte{}, err
	}

	k := types.Keg{}
	kegs := make([]types.Keg, 0)
	for rows.Next() {
		err := rows.Scan(&k.Id, &k.Name, &k.Tap, &k.Abv, &k.Capacity, &k.Remaining,
			&k.DateTapped, &k.DateKicked, &k.DaysToConsume, &k.Status)

		if err != nil {
			common_log.FancyHandleError(err)
			return []byte{}, err
		}

		fmt.Printf("%+v\n", k)
		kegs = append(kegs, k)
	}

	kegBytes, marshErr := json.Marshal(kegs)
	if marshErr != nil {
		common_log.FancyHandleError(marshErr)
	}

	return kegBytes, marshErr
}
