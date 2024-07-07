package common_db

import (
	"KegwatchApi/common_log"
	"KegwatchApi/types"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"log"
)

func GetAllUsers() ([]byte, error) {
	rows, err := GetDb().Query("SELECT id, body_cat from consumers")
	if err != nil {
		return []byte{}, err
	}

	u := types.User{}
	users := make([]types.User, 0)
	for rows.Next() {
		err := rows.Scan(&u.Id, &u.BodyCat)
		if err != nil {
			return []byte{}, err
		}

		fmt.Printf("%+v\n", u)
		users = append(users, u)
	}

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
		err := rows.Scan(&u.Id, &u.BodyCat, &u.Grams, &u.IsFemale)
		common_log.FailOnError(err, "failed to scan row to user struct")

		fmt.Printf("%+v\n", u)
		users = append(users, u)
	}

	return users
}

func InsertUser(u types.User) error {
	// Actual DB insertion
	insertQuery := fmt.Sprintf("INSERT INTO consumers(id, body_cat, grams) VALUES ('%+v', %d, %d)", u.Id, u.BodyCat, u.Grams)
	res, err := GetDb().Exec(insertQuery)
	if err != nil {
		return err
	}

	// Ensure everything went ok
	_, afterInsertErr := res.LastInsertId()

	return afterInsertErr
}
