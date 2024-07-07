package calc

import (
	"KwGameSvc/common_db"
	"KwGameSvc/common_log"
	"KwGameSvc/constants"
	"KwGameSvc/types"
	"encoding/json"
	"fmt"
	"strconv"
	"time"
)

const (
	ethanolDensity  = 0.789
	mlPerOz         = 29.5735
	gramsMetabPerHr = .015
)

var (
	logfile = "bac_calc.log"
	logger  = common_log.NewLoggerToFile(logfile)
)

func LogUsersBacs(players []types.Player, game types.Game) {
	for _, player := range players {
		LogUserBac(player, game)
	}
}

// Function to be called by REST endpoint when implemented
func LogUserBac(player types.Player, game types.Game) {
	bacUpdateTime := time.Now().Format(constants.TIME_FMT)

	// Drinks had since start of day
	fmt.Printf("\nPlayer id: %+v\n\n", player.GetID())
	drinks, err := common_db.GetDrinksInGame(player.GetID(), game)
	common_log.FailOnError(err, fmt.Sprintf("failed to get %+v's drinks in game %+v", player.Id, game.Description))

	// Don't waste time on it
	if len(drinks) < 1 {
		return
	}

	// Use drinks to calculate bac
	bac := CalculateBac(*player.User, drinks)
	fmt.Printf("\n\nBAC for %+v: %+v\n", player.GetID(), bac)

	insertErr := common_db.InsertBac(bac, player, game, bacUpdateTime)
	if insertErr != nil {
		common_log.FailOnError(insertErr, fmt.Sprintf("failed to insert BAC for %+v", player.GetID()))
	}
}

func CalculateBac(user types.User, drinks []types.Drink) float32 {
	// Aggregate current BAC from all drinks in game
	var newBac float32
	totalAbv := float32(0.0)
	totalOz := float32(0.0)

	for _, drink := range drinks {
		totalAbv += drink.Abv
		totalOz += drink.Oz

		newBac = AccountForDrinkBac(user, drink, newBac)
	}

	avgAbv := (totalAbv / float32(len(drinks)))
	logger.Infof("User %+v had %+voz averaging %+vpct abv. New BAC is %+v", user.Id, printableFloat(totalOz), printableFloat(avgAbv), printableFloat(newBac))

	drinkBytes, err := json.MarshalIndent(drinks, "", " ")
	if err == nil {
		logger.Infof("Here are the drinks: \n%+v\n", string(drinkBytes))
	} else {
		logger.Errorf("Failed to marshal drinks: %+v", err)
	}

	return newBac
}

func printableFloat(f float32) string {
	return strconv.FormatFloat(float64(f), 'f', 4, 32)
}

// Calculate and return current BAC impact from given drink at time
func AccountForDrinkBac(user types.User, drink types.Drink, carriedBac float32) float32 {
	gramsAlochol := (drink.Abv / 100) * (drink.Oz * mlPerOz) * ethanolDensity

	fmt.Printf("\ngramsAlcohol: %+v\n", gramsAlochol)

	pJson, err := json.Marshal(user)
	if err == nil {
		fmt.Printf("\nPlayer: %+v\n", string(pJson))
	}

	dJson, err := json.Marshal(drink)
	if err == nil {
		fmt.Printf("\nDrink: %+v\n", string(dJson))
	}

	// fmt.Printf("\n\ngramsAlcohol: %+vg\n", gramsAlochol)

	// Calculate BAC from this drink as pct
	rawBac := gramsAlochol / (float32(user.GetGrams()) * GetBacConstant(user.IsFemale))
	bacPct := rawBac * 100

	fmt.Printf("\nbacPct: %+v\n", bacPct)

	// Account for metabolization since time of drink
	fmt.Printf("\nDrink time: %+v\n", drink.Time.Format(constants.TIME_FMT))
	hrsSinceDrink := time.Since(drink.Time).Hours()
	fmt.Printf("\nhrsSinceDrink: %+v\n", hrsSinceDrink)

	bacAfterTime := bacPct - float32(hrsSinceDrink*gramsMetabPerHr)

	// Obviously the drink can't detract from BAC
	if bacAfterTime < 0 {
		bacAfterTime = 0
	}

	fmt.Printf("\nDrink at %+v currently has effect of %+v BAC on %+v\n======\n\n", drink.Time, bacAfterTime, user.Id)

	return bacAfterTime + carriedBac
}

func GetBacConstant(fem bool) float32 {
	if fem {
		return float32(types.FemBacConstant)
	}

	return float32(types.MaleBacConstant)
}
