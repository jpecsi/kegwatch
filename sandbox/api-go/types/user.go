package types

type User struct {
	Id       string `json:"id" db:"id"`
	BodyCat  int    `json:"body_cat" db:"body_cat"`
	Grams    int    `json:"grams" db:"grams"`
	IsFemale bool   `json:"is_female" db:"is_female"`
}

type UserPass struct {
	Name string  `json:"name"`
	Oz   int     `json:"oz"`
	Bac  float32 `json:"bac"`
	Beer string  `json:"beer"`
}
