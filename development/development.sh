#!/usr/bin/env bash

set -e

export ROOT_PATH=$(cd ../ && pwd)

if [[ $(sysctl vm.max_map_count) != *"262144"* ]]; then
    sudo sysctl -w vm.max_map_count=262144
fi

if [ ! -f "$ROOT_PATH/src/.env" ]; then
    cp "$ROOT_PATH/src/.env.example" "$ROOT_PATH/src/.env"
fi

echo "⬇️ Turning containers down"
docker compose -f $ROOT_PATH/development/docker-compose.yml down --remove-orphans
echo "🔨 Build containers"
docker compose -f $ROOT_PATH/development/docker-compose.yml build
echo "⬆️ Turning containers up"
docker compose -f $ROOT_PATH/development/docker-compose.yml --env-file "$ROOT_PATH/src/.env" up -d
echo "🎨 Applying code reformat"
docker exec -it document-hub-app black .
docker exec -it document-hub-app pylint .
