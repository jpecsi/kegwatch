package types

import "time"

type Drink struct {
	User   string    `json:"user_id" db:"user_id"`
	BeerId string    `json:"beer_id" db:"beer_id"`
	Time   time.Time `json:"time" db:"time"`
	Abv    float32   `json:"abv" db:"abv"`
	Oz     float32   `json:"oz" db:"oz"`
	// Time    string  `json:"time" db:"time"`
	// DateKicked    *string `json:"date_kicked" db:"date_kicked"`
	// DaysToConsume *int    `json:"days_to_consume,omitempty" db:"days_to_consume,omitempty"`
	// Status        int     `json:"status,omitempty" db:"status"`
}
