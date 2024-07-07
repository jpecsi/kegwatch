package common_http

import (
	"KwGameSvc/calc"
	"KwGameSvc/common_db"
	"KwGameSvc/common_log"
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"strings"

	"github.com/gorilla/mux"
)

const (
	bacPathSegment = "/bac"

	GET     = "GET"
	OPTIONS = "OPTIONS"

	bacPrecision = 3
)

var BacRoutes = Routes{
	Route{
		"GetBac",
		GET,
		bacPathSegment + "/user/{userId}",
		GetBac,
	},
}

type BacReading struct {
	BacPct float32 `json:"bac_pct"`
}

func GetBac(w http.ResponseWriter, r *http.Request) {
	logger.Infoln("In GetBac..")
	vars := mux.Vars(r)

	// Correct spaces in PK userId -
	//   (e.g. "Eli Harper")
	//   after extraction from the URL
	uid := vars["userId"]
	sanitizeSpaces(&uid)

	logger.Infoln("Getting user..")
	user, err := common_db.GetUser(uid)
	if err != nil {
		w.Write([]byte("failed to get user " + uid + " by id: " + err.Error()))
		w.WriteHeader(http.StatusBadRequest)
	}

	logger.Infoln("Getting drinks of the last 12 hours")
	drinks, drinkErr := common_db.GetDrinksWithImpact(uid)
	common_log.FailOnError(drinkErr,
		fmt.Sprintf("failed to get drinks user %+v has had in the last 12hrs", uid))

	roundedBac := roundFloat(calc.CalculateBac(user, drinks), bacPrecision)
	bacPct := BacReading{
		BacPct: roundedBac,
	}

	logger.Infof("Marshaling bac pct (%+v)", bacPct.BacPct)
	bacBytes, err := json.Marshal(bacPct)
	if err != nil {
		w.Write([]byte(fmt.Sprintf("failed to marshal BacReading: %+v", err.Error())))
		w.WriteHeader(http.StatusInternalServerError)

		return
	}

	logger.Infoln("All good; returning")
	w.Write(bacBytes)
	w.WriteHeader(http.StatusOK)
}

/* Helper Functions */
func sanitizeSpaces(uid *string) {
	*uid = strings.Replace(*uid, "%20", " ", -1)
	*uid = strings.Replace(*uid, "+", " ", -1)
}

// I don't like that this seems to be the best way to round a float32..
func roundFloat(val float32, precision uint) float32 {
	formatter := "%." + fmt.Sprintf("%d", precision) + "f"
	rndStr := fmt.Sprintf(formatter, val)

	s, err := strconv.ParseFloat(rndStr, 32)
	common_log.FailOnError(err, fmt.Sprintf("failed to parse %+v to float", rndStr))

	return float32(s)
}
