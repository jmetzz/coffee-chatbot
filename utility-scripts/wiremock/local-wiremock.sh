#!/bin/bash
# Script that starts a mock service to retrieve CRM data via wiremock
# See: http://wiremock.org/docs/running-standalone/

PORT=8080

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

while getopts ":hp:" opt; do
    case "${opt}" in
        h)
            usage
            exit 0
            ;;
        p)
            PORT=${OPTARG}
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

type wiremock >/dev/null 2>&1 || { echo >&2 "Wiremock is not installed. See http://wiremock.org. Aborting."; exit 2; }

echo
echo "Starting wiremock server"
echo "To stop the server user '^C' OR send a POST request with an empty body to http://<host>:<port>/__admin/shutdown"
echo
echo "  Example:"
echo "    1-  curl -X POST http://localhost:3000/__admin/shutdown"
echo "    2-  http post http://localhost:3000/__admin/shutdown"
echo
echo


wiremock --port "$PORT" --async-response-enabled true 2>&1

