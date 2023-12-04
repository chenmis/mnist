#!/usr/bin/env bash
set -e

NETWORK_NAME=mnist_net
docker network create ${NETWORK_NAME} || echo "Network ${NETWORK_NAME} already exists"
docker compose -f /Users/chen/PycharmProjects/GRPC-client/compose/server.yml -f /Users/chen/PycharmProjects/GRPC-client/compose/client.yml -p compose down
docker compose -f /Users/chen/PycharmProjects/GRPC-client/compose/server.yml -f /Users/chen/PycharmProjects/GRPC-client/compose/client.yml -p compose up --build -d
