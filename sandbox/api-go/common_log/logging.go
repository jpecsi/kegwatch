package common_log

import (
	"fmt"
	"io"
	"log"
	"os"
	"runtime"

	"github.com/sirupsen/logrus"
)

func NewLoggerToFile(filename string) *logrus.Logger {
	filename = "log/" + filename
	f, fileErr := os.OpenFile(filename,
		os.O_APPEND|os.O_CREATE|os.O_RDWR, 0755)

	logLevel := os.Getenv("LOG_LEVEL")
	logrusLevel, err := logrus.ParseLevel(logLevel)
	if err != nil {
		_ = fmt.Errorf("invalid log level provided: %+v", err)
		logrusLevel = logrus.DebugLevel
	}

	logger := &logrus.Logger{
		Out:   f,
		Level: logrusLevel,
	}

	// Assume this is unit testing where the logdir is not configured -
	//   we don't want to see errors spewed in this case; just discard output
	if fileErr != nil {
		logger.SetOutput(io.Discard)
	}

	logger.SetFormatter(&logrus.TextFormatter{
		ForceColors:     true,
		TimestampFormat: "2006-01-02 15:04:05.00",
		FullTimestamp:   true,
	})

	return logger
}

func InitLogrus(output string, loglevel logrus.Level) {
	f, err := os.OpenFile(output,
		os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Println(err)
	}

	logrus.SetOutput(f)
	logrus.SetLevel(loglevel)
}

func LogrusStdout(loglevel logrus.Level) {
	// Configure a formatter for standardization
	txtFmtr := logrus.TextFormatter{
		ForceColors:     true,
		TimestampFormat: "2006-01-02 15:04:05.00",
		FullTimestamp:   true,
	}

	logrus.SetLevel(loglevel)
	logrus.SetFormatter(&txtFmtr)
}

func FailOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

// this logs the function name as well.
func FancyHandleError(err error) (b bool) {
	if err != nil {
		// notice that we're using 1, so it will actually log the where
		// the error happened, 0 = this function, we don't want that.
		pc, filename, line, _ := runtime.Caller(1)

		log.Printf("[error] in %s[%s:%d] %v\n", runtime.FuncForPC(pc).Name(), filename, line, err)
		b = true
	}

	return
}
