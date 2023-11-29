#!/bin/bash

cleanup() {
    echo "Shutting down..."
    kill 0
}
trap 'cleanup' SIGINT

python3 session_handler.py & 

panel serve --setup setup.py --admin-log-level info --show --autoreload app.py & 

wait