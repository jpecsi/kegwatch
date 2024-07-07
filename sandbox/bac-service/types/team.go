package types

type TeamAffiliation struct {
	Game     string `json:"game" db:"game"`
	Consumer string `json:"consumer" db:"consumer"`
	Team     string `json:"team" db:"team"`
}
