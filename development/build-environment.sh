#!/usr/bin/env bash

set -e

export ROOT_PATH=$(cd ../ && pwd)

docker compose -f $ROOT_PATH/development/docker-compose.yml build
docker compose -f $ROOT_PATH/development/docker-compose.yml --env-file "$ROOT_PATH/src/.env" up -d
