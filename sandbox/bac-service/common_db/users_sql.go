package common_db

import (
	"KwGameSvc/common_log"
	"KwGameSvc/types"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"log"
)

func GetAllUsers() ([]byte, error) {
	rows, err := GetDb().Query("SELECT id, body_cat, grams, is_female from consumers")
	if err != nil {
		return []byte{}, err
	}

	users := RowsToUsers(rows)
	userBytes, marshErr := json.Marshal(users)
	if marshErr != nil {
		log.Fatalln(marshErr)
	}

	return userBytes, marshErr
}

func GetUser(id string) (types.User, error) {
	rows, err := GetDb().Query(fmt.Sprintf("SELECT id, body_cat, grams, is_female from consumers where id = '%+v'", id))
	if err != nil {
		return types.User{}, err
	}

	users := RowsToUsers(rows)
	if len(users) == 1 {
		return users[0], nil
	}

	return types.User{}, errors.New("no user found with id " + id)
}

func RowsToUsers(rows *sql.Rows) []types.User {
	u := types.User{}
	users := make([]types.User, 0)

	for rows.Next() {
		// To accept nil grams values and pass to setter accessor (private field grams)
		var g *int = nil

		// Read user info in
		err := rows.Scan(&u.Id, &u.BodyCat, &g, &u.IsFemale)
		common_log.FailOnError(err, "failed to scan row to user struct")

		// Set grams if not null in mysql
		logger.Infof("Deserialized sql data for user: \n\t%+v\n", u)
		if g != nil {
			u.SetGrams(g)
		}

		users = append(users, u)
	}

	return users
}
