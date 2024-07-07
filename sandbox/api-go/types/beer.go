package types

type Beer struct {
	PourTime string  `json:"time" db:"time"`
	TapId    int     `json:"tap_id" db:"tap_id"`
	Consumer string  `json:"consumer" db:"consumer"`
	OzPoured float32 `json:"oz_poured" db:"oz_poured"`

	BeerId   string `json:"beer_id,omitempty" db:"beer_id,omitempty"`
	BeerName string `json:"beer_name,omitempty" db:"beer_name,omitempty"`
}
