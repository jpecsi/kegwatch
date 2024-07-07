package routes

import (
	"KegwatchApi/common_log"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/rs/cors"
)

var (
	logfile = "http_server.log"
	logger  = common_log.NewLoggerToFile(logfile)
)

var routes []Route

type Route struct {
	Name        string
	Method      string
	Pattern     string
	HandlerFunc http.HandlerFunc
}

type Routes []Route

func ServeHttp() {
	collectRoutes()

	router := mux.NewRouter()

	// Serve routes using the RestLogger and middleware wrapper
	//   for route/request logging and authentication interception
	for _, route := range routes {
		fmt.Printf("\n - %+v: %+v\n", route.Method, route.Pattern)
		var handler http.Handler
		handler = route.HandlerFunc

		// Handle each route using a web server logger:
		handler = RestLogger(handler, route.Name)

		router.
			Methods(route.Method).
			Path(route.Pattern).
			Name(route.Name).
			Handler(handler)
	}

	// Lax CORS restrictions for "development mode":
	c := cors.New(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowedHeaders:   []string{"*"},
		AllowedMethods:   []string{"DELETE", "GET", "POST", "PUT", "OPTIONS"},
		AllowCredentials: true,
	})
	handler := c.Handler(router)

	// Serve itt
	log.Fatalln(http.ListenAndServe("0.0.0.0:8080", handler))
}

func collectRoutes() {
	routes = append(routes, BeerRoutes...)
	routes = append(routes, GameRoutes...)
	routes = append(routes, KegRoutes...)
	routes = append(routes, TeamRoutes...)
	routes = append(routes, UserRoutes...)
}

func RestLogger(inner http.Handler, name string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		inner.ServeHTTP(w, r)

		logger.Infof(
			"%s\t%s\t%s\t%s",
			r.Method,
			r.RequestURI,
			name,
			time.Since(start),
		)
	})
}

/* Helper functions */
