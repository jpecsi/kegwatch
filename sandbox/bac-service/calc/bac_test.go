package calc_test

import (
	"KwGameSvc/calc"
	"KwGameSvc/types"
	"testing"
	"time"
)

var (
	gramsPerPound = 453.592
)

func TestAccountForDrinkBac(t *testing.T) {
	g := int(180 * gramsPerPound)

	me := &types.User{
		Id:       "Eli Harper",
		BodyCat:  1,
		Grams:    &g,
		IsFemale: false,
	}

	mePlayer := types.NewPlayer()
	mePlayer.Team = "Team 1"
	mePlayer.User = me

	bigAssDrinky := types.Drink{
		BeerId: "125b44ac-5e0c-4be0-96da-01c70edfba71",
		User:   me.Id,
		Time:   time.Now(),
		Oz:     (5 * 12), // 5 "drinks"
		Abv:    5,        //Round
	}

	newBac := calc.AccountForDrinkBac(*mePlayer.User, bigAssDrinky, 0.0)
	bigAssExpected := 0.12608317
	if newBac != float32(bigAssExpected) {
		t.Errorf("AccountForDrinkBac didn't return expected value of %+v - got: %+v", bigAssExpected, newBac)
	}

	bigAssDrinky2 := types.Drink{
		BeerId: "125b44ac-5e0c-4be0-96da-01c70edfba71",
		User:   me.Id,
		Time:   time.Now().Add(-(4 * time.Hour)),
		Oz:     (8 * 12), // 8 "drinks"
		Abv:    5,        // Nice and round for checking against
	}

	bacAfterFourHrs := calc.AccountForDrinkBac(*mePlayer.User, bigAssDrinky2, 0.0)
	expectedAfterFour := 0.14173308

	if bacAfterFourHrs != float32(expectedAfterFour) {
		t.Errorf("\n\nAfter 8 drinks over 4 hours; expected %+v, but got: %+v", expectedAfterFour, bacAfterFourHrs)
	}
}
