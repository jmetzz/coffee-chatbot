#!/usr/bin/env bash

set -e

banner() {
    msg="| $* |"
    edge=$(echo "$msg" | sed 's/./~/g')
    echo "$edge"
    echo "$msg"
    echo "$edge"
}

function usage {
    banner "                                Usage                              "
    echo "Available options:"
    echo "     chatette    - generate nlu input data based on chatette"
    echo "     augment     - augment stories base on rules"
    echo "     generate    - chatette + augment"
    echo "     verify      - will verify input data"
    echo "     train       - will train the rasa models"
    echo "     evaluate    - will evaluate the rasa dialogue model"
    echo "     run         - will start the rasa dialogue server"
    echo
}

function error {
    echo "$2" >&2
    usage
    exit $1
}



function process_chatette(){
    if [[ -f ./data/chatette/master.chatette ]]; then
        mkdir -p ./data/temp_chatette_output
        python -m chatette ./data/chatette/master.chatette -o ./data/temp_chatette_output -s ANYSEED
        mkdir -p ./data/nlu
        mv ./data/temp_chatette_output/train/* ./data/nlu
        if [[ -d ./data/temp_chatette_output/test ]]; then
            mkdir -p ./data/nlu_test_data
            mv ./data/temp_chatette_output/test/* ./data/nlu_test_data
        fi
        rm -rf ./data/temp_chatette_output
    fi
}

function augment_stories(){
    stories_path="${1}"
    rules="${2}"
    out_path="${3}"
    out_file="${4}"

    [[ ! -d "${stories_path}" ]] && error 4 "stories to augment not found. Check the given path: ${stories_path}"
    [[ ! -f "${rules}" ]] && error 4 "Augmentation rules file not found. Check the given filename: ${rules}"

    mkdir -p $out_path
    python "$SRC"/stories_aug_app.py -s $stories_path -r $rules -o "${out_path}/${out_file}"
    echo "Augmented stories: ${out_path}/${out_file}"
}


CORE_DEBUG=""
while getopts ":hd" opt; do
    case "${opt}" in
        d)
            export CORE_DEBUG="--debug-plots"
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
[[ ${#remaining_arguments[*]} -ne 1 ]] && error 3 "Missing sub-task"


source activate coffee-bot
#export LD_LIBRARY_PATH=/usr/local/lib64/:$CONDA_PREFIX/lib
#export LD_PRELOAD=$CONDA_PREFIX/lib/libstdc++.so
SRC="./src/main/python"


case ${remaining_arguments[0]} in
    chatette)
        process_chatette
        ;;
    augment)
        augment_stories './data/core/aug_base_stories' './config/rules.yml' './data/core/stories' '__augmented_stories__.md'
        ;;
    generate)
        banner "Generating NLU data"
        process_chatette
        echo
        banner "Generating CORE data"
        augment_stories './data/core/aug_base_stories' './config/rules.yml' './data/core/stories' '__augmented_stories__.md'
        ;;
    verify)
        python "$SRC"/utils/verify.py
        ;;
    train)
        rasa train -c $CONFIG_FILE -d $DOMAIN_FILE $DEBUG --data $DATA_PATH nlu core
        ;;
    evaluate)
        export PYTHONPATH="${PYTHONPATH}:$SRC"
        python "$SRC"/evaluation/evaluate.py
        ;;
    run)
        echo "Not implemented yet"
        ;;
    *)
        echo
        echo "*** Unknown option:" ${1}
        usage
        ;;
esac

