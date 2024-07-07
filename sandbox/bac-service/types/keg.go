package types

type Keg struct {
	Id            string  `json:"id,omitempty" db:"id"`
	Name          string  `json:"name" db:"name"`
	Tap           int     `json:"tap" db:"tap"`
	Abv           float32 `json:"abv" db:"abv"`
	Capacity      int     `json:"capacity" db:"capacity"`
	Remaining     float32 `json:"remaining,omitempty" db:"remaining"`
	DateTapped    string  `json:"date_tapped" db:"date_tapped"`
	DateKicked    *string `json:"date_kicked" db:"date_kicked"`
	DaysToConsume *int    `json:"days_to_consume,omitempty" db:"days_to_consume,omitempty"`
	Status        int     `json:"status,omitempty" db:"status"`
}
