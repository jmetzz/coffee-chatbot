## chitchat
# TODO

## deny ask_what_is_possible
* ask_what_is_possible
    - action_chitchat
* deny
    - utter_nohelp

## ask_what_is_possible
* greet
    - utter_greet
* ask_what_is_possible
    - action_chitchat

## ask_what_is_possible more
* greet
    - utter_greet
* ask_what_is_possible
    - action_chitchat
* ask_what_is_possible
    - action_chitchat
* bye
    - utter_bye


## just newsletter + confirm
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
    - form{"name": null}
* affirm
    - utter_thumbsup
    - utter_anything_else

## just newsletter, continue, + confirm
# TODO

## just newsletter, don't continue, + confirm
# TODO


## just newsletter (with email already) + confirm
# TODO


## just newsletter, continue
# TODO


## just newsletter, don't continue
# TODO

