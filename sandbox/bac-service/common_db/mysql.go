package common_db

import (
	"KwGameSvc/common_log"
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/go-sql-driver/mysql"
)

var (
	db         *sql.DB
	connectErr error

	logfile = "sql.log"
	logger  = common_log.NewLoggerToFile(logfile)

	u = "root"
	p = "ilovejesus"
	a = "kegwatch_db:3306"
	d = "kegwatch"
)

type RawTime []byte

func (t RawTime) Time() time.Time {
	ti, err := time.Parse("2006-01-02 15:04:05", string(t))
	common_log.FailOnError(err, "failed to parse mysql time")

	// UTC - EST hack; remove asap
	ti = ti.Add(5 * time.Hour)

	return ti
}

/* Managerial & Helper Functions */

func GetDb() *sql.DB {
	if db != nil {
		return db
	}

	db, connectErr = OpenConnection()
	common_log.FailOnError(connectErr, "failed to open connection to db in GetDb()")

	return db
}

func OpenConnection() (*sql.DB, error) {
	fmt.Printf("Opening connection with credentials:\nUser:\t%+v\n"+
		"Pass:\t%+v\nAddr:\t%+v\nDb:\t%+v\n", u, p, a, d)

	// Capture connection properties.
	cfg := mysql.Config{
		User:   u,
		Passwd: p,
		Net:    "tcp",
		Addr:   a,
		DBName: d,
	}

	db, connectErr = sql.Open("mysql", cfg.FormatDSN())
	if connectErr != nil {
		return db, connectErr
	}

	pingErr := db.Ping()
	if pingErr == nil {
		fmt.Println("Ping success")
	}

	return db, pingErr
}

func VerifyDbConn(r *http.Request) {
	if db == nil {
		// Re-attempt to connect:
		db, connectErr = OpenConnection()

		// Still failling? Shut it down so we know something's fucky
		if db == nil || connectErr != nil {
			r.Response.StatusCode = http.StatusInternalServerError
			log.Fatalf("database connection isn't alive - error: %+v", connectErr)
		}
	}
}

/* Credential setters */
func SetUser(user string) {
	u = user
}

func SetPw(pw string) {
	p = pw
}

func SetAddr(addr string) {
	a = addr
}

func SetDb(db string) {
	d = db
}
