package constants

const (
	// REST Constants:
	DELETE  = "DELETE"
	GET     = "GET"
	OPTIONS = "OPTIONS"
	POST    = "POST"
	PUT     = "PUT"

	// Time constants:
	DATE_FMT = "2006-01-02"
	TIME_FMT = "2006-01-02 15:04:05"
)

type Status int

const (
	Inactive Status = iota
	Active
)
