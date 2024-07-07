package main

import (
	"KwGameSvc/calc"
	"KwGameSvc/common_db"
	"KwGameSvc/common_http"
	"KwGameSvc/common_log"

	"os"
	"time"
)

type Drinkstamp struct {
	TimePoured   *time.Time
	TimeFinished *time.Time
	Abv          float32
	FlOz         float32
}

func main() {
	/* Get MySQL credentials from docker run -e env vars */
	scrapeSqlEnvs()

	/* Continue with real program logic */
	db, connectErr := common_db.OpenConnection()
	common_log.FailOnError(connectErr, "failed to open a connection to the db; shutting down..")
	defer db.Close()

	// Serve HTTP endpoint
	go common_http.ServeHttp()

	games, err := common_db.GetActiveGames()
	common_log.FailOnError(err, "failed to fetch active games; shutting down")

	// Poll every 5m and log all drinks
	for {
		for _, game := range games {
			players, err := common_db.GetPlayersOfGame(game.Id)
			common_log.FailOnError(err, "Failed to get players of the game "+game.Description)

			calc.LogUsersBacs(players, game)
		}

		time.Sleep(5 * time.Minute)
	}
}

func scrapeSqlEnvs() {
	u := os.Getenv("USER")
	if u != "" {
		common_db.SetUser(u)
	}

	p := os.Getenv("PW")
	if p != "" {
		common_db.SetPw(p)
	}

	a := os.Getenv("ADDR")
	if a != "" {
		common_db.SetAddr(a)
	}

	d := os.Getenv("DB")
	if d != "" {
		common_db.SetDb(d)
	}
}
