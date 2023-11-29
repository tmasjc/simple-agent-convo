#!/bin/bash

cleanup() {
    echo "Shutting down..."
    kill 0
}
trap 'cleanup' SIGINT

python3 session_handler.py &

panel serve app.py \
    --setup setup.py --admin-log-level info \
    --basic-auth 0000 --cookie-secret simple_cookie \
    --basic-login-template www/login.html \
    --logout-template www/logout.html \
    --static-dirs assets=./assets \
    --show --autoreload &

wait
