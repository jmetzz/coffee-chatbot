#!/usr/bin/env bash

PORT=8080
MAPPINGS=$(pwd)

function usage {
    name=$(basename $0)
    echo "$name [options]"
    echo
    echo "  Options:"
    echo "       -h shows this message"
    echo "       -p port to start the server (Default: 8080)"
    echo
}

function error {
    echo "$2" >&2
    usage
    exit $1
}

while getopts ":hm:p:" opt; do
    case "${opt}" in
        h)
            usage
            exit 0
            ;;
        p)
            PORT=${OPTARG}
            ;;
        m)
            MAPPINGS=${OPTARG}
            ;;
        :)
            error 2 "Option -$OPTARG requires an argument."
            ;;
        \?)
            error 1 "Invalid option: -$OPTARG"
            ;;
    esac
done
shift $((OPTIND-1))

remaining_arguments=( "$@" )
[[ ${#remaining_arguments[*]} -gt 0 ]] && error 1 "Invalid arguments"

docker run -it --rm -p $PORT:8080 -v $MAPPINGS:/home/wiremock jmetzz/wiremock