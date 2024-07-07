package routes

import (
	"KegwatchApi/common_db"
	"KegwatchApi/common_log"
	"KegwatchApi/constants"
	"KegwatchApi/types"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/gorilla/mux"
)

const (
	kegsPathSegment = "/kegs"
)

var KegRoutes = Routes{
	Route{
		"GetKegs",
		constants.GET,
		kegsPathSegment,
		GetActiveKegs,
	},
	Route{
		"GetAllKegs",
		constants.GET,
		kegsPathSegment + "/all",
		GetAllKegs,
	},
	Route{
		"CreateKeg",
		constants.POST,
		kegsPathSegment,
		CreateKeg,
	},
	Route{
		"KickKeg",
		constants.PUT,
		kegsPathSegment + "/kick/{tapNo}",
		KickKeg,
	},
}

type KegErr struct {
	Error       string     `json:"error"`
	PreviousKeg *types.Keg `json:"previous_keg"`
}

// GetActiveKegs godoc
// @Summary    Get Active kegs
// @Description  Gets ACTIVE kegs stored in DB, represented in JSON format
// @Tags         kegs
// @Accept       json
// @Produce      json
// @Success      200  {array}  types.Keg
// @Failure      404
// @Failure      500  {object}  string
// @Router       /kegs [GET]
func GetActiveKegs(w http.ResponseWriter, r *http.Request) {
	common_db.VerifyDbConn(r)

	kegBytes, err := common_db.GetActiveKegs()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	_, writeErr := w.Write(kegBytes)
	common_log.FancyHandleError(writeErr)
}

// GetAllKegs godoc
// @Summary    Get all kegs
// @Description  Gets all kegs stored in DB, represented in JSON format
// @Tags         kegs
// @Accept       json
// @Produce      json
// @Success      200  {array}  types.Keg
// @Failure      404
// @Failure      500  {object}  string
// @Router       /kegs/all [GET]
func GetAllKegs(w http.ResponseWriter, r *http.Request) {
	common_db.VerifyDbConn(r)

	kegBytes, err := common_db.GetAllKegs()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	_, writeErr := w.Write(kegBytes)
	common_log.FancyHandleError(writeErr)
}

// CreateKeg godoc
// @Summary     Create a keg
// @Description  	Creates a single keg as indicated by the JSON provided in the POST request body
// @Tags         	kegs
// @Accept       json
// @Produce      text/plain
// @Param     	keg body types.Keg true "The keg to be added to the database"
// @Success      200
// @Failure      400  {object}  string
// @Failure      404
// @Failure      500  {object}  string
// @Router       /kegs [POST]
func CreateKeg(w http.ResponseWriter, r *http.Request) {
	// We're looking for a post - the pre-flight request is stupid, short-circuit now lol
	if r.Method == http.MethodOptions {
		return
	}

	common_db.VerifyDbConn(r)

	// Body -> Keg struct conversion
	var k types.Keg
	err := json.NewDecoder(r.Body).Decode(&k)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Ensure the tap is free
	if k.Status == int(constants.Active) {
		if prevKeg := common_db.KegInTap(k.Tap); prevKeg != nil {
			w.WriteHeader(http.StatusBadRequest)

			e := errors.New("this keg was previously in the tap - ensure it's deactivated (and empty) before proceeding.. No beer left behind ;) ")
			ke := &KegErr{
				Error:       e.Error(),
				PreviousKeg: prevKeg,
			}

			keBytes, err := json.Marshal(ke)
			if err != nil {
				fmt.Printf("failed to marshal keg error: %+v", err)
			}

			w.Write(keBytes)
			return
		}
	}

	// TypeScript strictness requires this type of number handling
	//   -- MySQL def is default null
	if k.DaysToConsume == nil || *k.DaysToConsume < 1 {
		k.DaysToConsume = nil
	}

	// Defensively populate the date tapped if it's not provided
	todayDateTapped := time.Now().Format(constants.DATE_FMT)
	if k.DateTapped == nil || len(*k.DateTapped) == 0 {
		k.DateTapped = &todayDateTapped
	}

	// Set remaining to capacity if not provided
	if k.Remaining == nil || (*k.Remaining == 0.0 && k.DateTapped == &todayDateTapped) {
		allRemaining := float32(k.Capacity)
		k.Remaining = &allRemaining
	}

	id, afterInsertErr := common_db.InsertKeg(k)
	if afterInsertErr != nil {
		http.Error(w, afterInsertErr.Error(), http.StatusInternalServerError)

		// Barf
		log.Printf("Error returned while performing db insert: %+v", afterInsertErr.Error())

		return
	}

	// We good
	w.Write([]byte(id))
	w.WriteHeader(http.StatusOK)
}

// KickKeg godoc
// @Summary     Mark a keg as "kicked" or empty
// @Description  	Updates a single keg as indicated by the JSON provided in the POST request body, giving it a 'date kicked' and 'days to consume'
// @Tags         	kegs
// @Accept       json
// @Produce      text/plain
// @Param     	tapNo path int true "The keg's tap number"
// @Success      200
// @Failure      400  {object}  string
// @Failure      404
// @Failure      500  {object}  string
// @Router       /kegs/kick/{tapNo} [PUT]
func KickKeg(w http.ResponseWriter, r *http.Request) {
	// We're looking for a post - the pre-flight request is stupid, short-circuit now lol
	if r.Method == http.MethodOptions {
		return
	}

	// Snatch the url param
	vars := mux.Vars(r)
	tapNo := vars["tapNo"]

	common_db.VerifyDbConn(r)

	// Cast the tapNo parameter to int
	tapInt, convErr := strconv.Atoi(tapNo)
	common_log.FancyHandleError(convErr)

	// Fetch the keg we're referencing
	k, err := common_db.GetActiveKegByTapNo(tapInt)
	common_log.FancyHandleError(err)

	// Ensure the tap is free
	if k.Status == int(constants.Active) {
		k.Status = int(constants.Inactive)
	}

	kickErr := common_db.KickKeg(*k.Id, *k.DateTapped)
	if kickErr != nil {
		retErr := errors.New(fmt.Sprintf("Error returned while kicking keg in the DB: %+v", kickErr.Error()))
		http.Error(w, retErr.Error(), http.StatusInternalServerError)

		// Barf
		log.Printf(retErr.Error())
		return
	}

	// We good
	w.Write([]byte(*k.Id))
	w.WriteHeader(http.StatusOK)
}
