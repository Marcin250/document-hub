#!/usr/bin/env bash

set -e

export ROOT_PATH=$(cd ../ && pwd)

if [[ $(sysctl vm.max_map_count) != *"262144"* ]]; then
    sudo sysctl -w vm.max_map_count=262144
fi

if [ ! -f "$ROOT_PATH/src/.env" ]; then
    echo "1"
    cp "$ROOT_PATH/src/.env.example" "$ROOT_PATH/src/.env"
fi

docker compose -f $ROOT_PATH/development/docker-compose.yml down --remove-orphans

eval "${ROOT_PATH}/development/build-environment.sh"
