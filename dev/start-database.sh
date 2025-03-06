#!/usr/bin/env bash

CONTAINER_NAME="csi3450-bank"
POSTGRES_IMAGE="postgres:latest"

DATABASE_PORT=5432
DATABASE_NAME="bank"
DATABASE_USER="postgres"
DATABASE_PASSWORD="postgres"

HOST_PORT=5432

is_container_running() {
    docker ps --filter "name=^/${CONTAINER_NAME}$" --filter "status=running" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"
}

container_exists() {
    docker ps -a --filter "name=^/${CONTAINER_NAME}$" --format '{{.Names}}' | grep -q "${CONTAINER_NAME}"
}

is_port_in_use() {
    lsof -i :${HOST_PORT} &>/dev/null
}

if is_container_running; then
    echo "Container '${CONTAINER_NAME}' is already running."
    exit 0
fi

if is_port_in_use; then
    echo "Port ${HOST_PORT} is already in use. Please choose a different port or stop the process using it."
    exit 1
fi

if container_exists; then
    echo "Container '${CONTAINER_NAME}' exists but is not running. Restarting it..."
    docker start ${CONTAINER_NAME}
    if [ $? -eq 0 ]; then
        echo "Container '${CONTAINER_NAME}' restarted successfully."
        exit 0
    else
        echo "Failed to restart the container."
        exit 1
    fi
fi

echo "Starting a new PostgreSQL container..."
docker run -d \
    --name ${CONTAINER_NAME} \
    -e POSTGRES_USER=${DATABASE_USER} \
    -e POSTGRES_PASSWORD=${DATABASE_PASSWORD} \
    -e POSTGRES_DB=${DATABASE_NAME} \
    -p ${HOST_PORT}:${DATABASE_PORT} \
    ${POSTGRES_IMAGE}

if [ $? -eq 0 ]; then
    echo "PostgreSQL container '${CONTAINER_NAME}' started successfully on port ${HOST_PORT}."
else
    echo "Failed to start the PostgreSQL container."
    exit 1
fi

