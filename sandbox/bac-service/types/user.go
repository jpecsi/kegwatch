package types

type User struct {
	Id       string `json:"id" db:"id"`
	BodyCat  int    `json:"body_cat" db:"body_cat"`
	Grams    *int   `json:"grams" db:"grams"`
	IsFemale bool   `json:"is_female" db:"is_female"`
}

type Player struct {
	*User
	Team string
}

func NewPlayer() Player {
	user := User{}
	return Player{
		User: &user,
	}
}

func NewUser(id string, bodyCat int, g *int, isFem bool) User {
	return User{
		Id:       id,
		BodyCat:  bodyCat,
		Grams:    g,
		IsFemale: isFem,
	}
}

func (p Player) GetID() string {
	return p.Id
}

func (p Player) GetBodyCat() int {
	return p.BodyCat
}

func (u User) GetBodyCat() int {
	return u.BodyCat
}

func (u User) GetIsFemale() bool {
	return u.IsFemale
}

func (u User) GetGrams() int {
	if u.Grams != nil && *u.Grams > 0 {
		return *u.Grams
	}

	return u.ApproximateMass()
}

func (u *User) SetGrams(g *int) {

	if g != nil {
		u.Grams = g
	}
}

type Person interface {
	GetID() string
	GetBodyCat() int
	GetGrams() int
	GetIsFemale() bool
}

type BodyCat int

const (
	Petite BodyCat = iota
	Average
	Large
)

type BacConstant float32

const (
	FemBacConstant  BacConstant = 0.55
	MaleBacConstant BacConstant = 0.68
)

type MassApproximation map[BodyCat]int

var (
	// * 454 converts from lbs to g
	MaleMassApproximator MassApproximation = MassApproximation{
		Petite:  130 * 454,
		Average: 170 * 454,
		Large:   200 * 454,
	}

	FemaleMassApproximator MassApproximation = MassApproximation{
		Petite:  90 * 454,
		Average: 120 * 454,
		Large:   160 * 454,
	}
)

func (u User) ApproximateMass() int {
	if u.GetIsFemale() {
		return FemaleMassApproximator[BodyCat(u.GetBodyCat())]
	}

	return MaleMassApproximator[BodyCat(u.GetBodyCat())]
}
