package types_test

import (
	"KwGameSvc/types"
	"testing"
)

func TestApproximateMass(t *testing.T) {
	// Man with average build
	u := types.NewUser("", int(types.Average), nil, false)
	m := u.ApproximateMass()

	if m < 0 {
		t.Errorf("Mass approximation is negative: %+v", m)
	}

	t.Logf("Mass approximation for an average male is: %+v", m)
}
func TestSetUserGrams(t *testing.T) {
	// My grams lol ~185lbs
	g := 83914
	u := types.NewUser("", int(types.Average), nil, false)

	u.SetGrams(&g)
	newGrams := u.GetGrams()
	if newGrams != g {
		t.Errorf("New grams isn't what it was set to: %+v != %+v", newGrams, g)
	}
}
