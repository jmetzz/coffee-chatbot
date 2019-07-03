#!/usr/bin/env bash


function usage {
    echo "$0 [OPTIONS]"
    echo "       -n train the NLU model (Default: false)"
    echo "       -c train the Dialogue model (Default: false)"
    echo "       -e evaluate the model (Default: false)"
    echo "       -v verify the input data (Default: false)"
    echo "       -d show debug plots when training core (Default: false)"
    echo "       -h shows this message"
    echo
}

function error {
    echo "$2" >&2
    usage
    exit $1
}

GENERATE_DATA=0
TRAIN_NLU=0
TRAIN_CORE=0
CORE_DEBUG=""
EVALUATE=0
VERIFY=0


while getopts ":hgnevd" opt; do
    case "${opt}" in
        g)
            GENERATE_DATA=1
            ;;

        n)
            TRAIN_NLU=1
            ;;
        c)
            TRAIN_CORE=1
            ;;
        e)
            EVALUATE=1
            ;;
        v)
            VERIFY=1
            ;;
        d)
            CORE_DEBUG="--debug-plots"
            ;;
        h)
            usage
            exit 0
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
[[ ${#remaining_arguments[*]} -ne 0 ]] && error 3 "Unknown argument"


# Set the environment variables needed to run
if [[ -f ".env" ]]; then
    source .env
else
    error 3 "\t.env file not found. Create the file and define the necessary variables (see endpoint.py)"
fi

# activate the conda dialogue environment
#source activate coffee-bot

function process_chatette(){
    if [[ -f ./data/chatette/master.chatette ]]; then
        mkdir -p ./data/temp_chatette_output
        python -m chatette ./data/chatette/master.chatette -o ./data/temp_chatette_output -s SEED
        [[ ! -d ./data/nlu ]] && mkdir -p ./data/nlu
        mv ./data/temp_chatette_output/train/* ./data/nlu
        if [[ -d ./data/temp_chatette_output/test ]]; then
            mkdir -p ./data/nlu_test_data
            mv ./data/temp_chatette_output/test/* ./data/nlu_test_data
        fi
        rm -rf ./data/temp_chatette_output
    fi
}

function generate_data(){
    process_chatette
    # Add stories augmentation to
}

[[ GENERATE_DATA == 1 ]] && generate_data
[[ $TRAIN_NLU == 1 ]] && rasa train -c $CONFIG_FILE -d $DOMAIN_FILE $DEBUG --data $DATA_PATH nlu
[[ $TRAIN_CORE == 1 ]] && rasa train -c $CONFIG_FILE -d $DOMAIN_FILE $DEBUG --data $DATA_PATH core


if [[ $VERIFY == 1 ]]; then
#    if [[ ! -d "./data" ]]; then
#        error 4 "No data directory available to verify the model"
#    fi
    echo "Verification step is not implemented yet"
fi

if [[ $EVALUATE == 1 ]]; then
    # Evaluate the dialogue model using the test_stories_strict and test_stories folders
    echo "Model evaluation is not implemented yet"
fi
