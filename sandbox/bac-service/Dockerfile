ARG arch arch
ARG arm arm

## Build
FROM golang:1.19.3-buster AS build

ARG arch
ARG arm

WORKDIR /app

COPY go.* .
RUN --mount=type=cache,target=/go/pkg/mod \
  go mod download

COPY . .

RUN --mount=target=. \
  --mount=type=cache,target=/root/.cache/go-build \
  --mount=type=cache,target=/go/pkg/mod \
  env GOOS=linux GOARCH=${arch} ${arm} go build -o /kw-game-svc main.go

## Deploy
FROM gcr.io/distroless/base-debian10

WORKDIR /

COPY --from=build /kw-game-svc /kw-game-svc

USER nonroot:nonroot

ENTRYPOINT ["/kw-game-svc"]