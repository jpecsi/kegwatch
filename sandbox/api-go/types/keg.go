package types

type Keg struct {
	Id *string `json:"id,omitempty" db:"id"`

	Abv      float32 `json:"abv" db:"abv"`
	Capacity int     `json:"capacity" db:"capacity"`
	Name     string  `json:"name" db:"name"`
	Tap      int     `json:"tap" db:"tap"`

	Remaining     *float32 `json:"remaining,omitempty" db:"remaining"`
	DateKicked    *string  `json:"date_kicked,omitempty" db:"date_kicked,omitempty"`
	DateTapped    *string  `json:"date_tapped,omitempty" db:"date_tapped"`
	DaysToConsume *int     `json:"days_to_consume,omitempty" db:"days_to_consume,omitempty"`

	Status int `json:"status" db:"status"`
}
