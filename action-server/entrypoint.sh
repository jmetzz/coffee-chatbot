#!/usr/bin/env bash

set -e

source activate coffee-bot-action
#export LD_LIBRARY_PATH=/usr/local/lib64/:$CONDA_PREFIX/lib
#export LD_PRELOAD=$CONDA_PREFIX/lib/libstdc++.so
case ${1} in
    run)
        SRC="./src/main/python"
        SERVER_PORT=5055
        LOGGING_CONFIG=./src/main/resources/config/logging_config.dev.ini
        NUMBER_OF_WORKERS=1
        GUNICORN_TIMEOUT=120
        exec gunicorn --bind :$SERVER_PORT --workers $NUMBER_OF_WORKERS --timeout $GUNICORN_TIMEOUT --log-config $LOGGING_CONFIG --pythonpath $SRC application:app
        ;;
    debug)
        echo "Action server not started yet. You should start it manually. Ex:"
        echo "gunicorn --bind :$SERVER_PORT --workers $NUMBER_OF_WORKERS --timeout $GUNICORN_TIMEOUT --log-config $LOGGING_CONFIG --pythonpath $SRC application:app"
        echo
        echo "Current conda environment is:"
        conda env list
        /bin/bash
        ;;
    *)
        echo "Got:" ${1}
        print_help
        ;;
esac
