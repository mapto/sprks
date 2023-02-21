#!/usr/bin/env bash

docker pull mariadb/server

docker run --name sprksdb -e MYSQL_ROOT_PASSWORD=1234 -d mariadb/server
