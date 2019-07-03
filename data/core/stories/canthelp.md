## greet
* greet
    - utter_greet

## greet + newsletter + canthelp + continue #TODO 
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue_newsletter
* affirm
    - utter_great
    - subscribe_newsletter_form
    - form{"name": null}

## greet + newsletter + canthelp + don't continue #TODO 
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue_newsletter
* deny
    - utter_thumbsup
    - action_deactivate_form
    - form{"name": null}

## Test

* ask_for_the_blog
    - utter_ask_for_the_blog
* ask_location
    - utter_ask_location
* ask_portfolio
    - utter_ask_portfolio
* ask_culture
    - utter_ask_culture
* thank
    - utter_anything_else
* deny
    - utter_thumbsup
* bye
    - utter_bye

## chitchat
* canthelp
    - utter_canthelp

## greet + canthelp
* greet
    - utter_greet
* canthelp
    - utter_canthelp

##TODO 
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue_newsletter
* affirm
    - utter_great
    - subscribe_newsletter_form
    - form{"name": null}
