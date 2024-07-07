## Build
FROM golang:1.19.3-alpine3.16 AS build

WORKDIR /app

COPY go.* ./
RUN --mount=type=cache,target=/go/pkg/mod \
  go mod download

COPY . ./

RUN --mount=target=. \
  --mount=type=cache,target=/root/.cache/go-build \
  --mount=type=cache,target=/go/pkg/mod \
  go build -o /kegwatch-api main.go

## Deploy
FROM gcr.io/distroless/base-debian10

WORKDIR /

COPY --from=build /kegwatch-api /kegwatch-api

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/kegwatch-api"]
