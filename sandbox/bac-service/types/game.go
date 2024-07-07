package types

type Game struct {
	Id          string `json:"id" db:"id"`
	Description string `json:"description" db:"description"`
	Date        string `json:"date" db:"date"`
	Status      int    `json:"status" db:"status"`
}
