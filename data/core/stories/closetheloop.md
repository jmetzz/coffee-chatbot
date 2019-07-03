## story number 1
* greet
    - utter_greet
* out_of_scope
    - utter_out_of_scope
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
    - form{"name": null}
* thank
    - utter_no_worries
    - utter_anything_else

## story number 2
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
    - form{"name": null}
* out_of_scope
    - utter_thumbsup
    - utter_anything_else

## story number 4
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
    - form{"name": null}
* thank
    - utter_no_worries
    - utter_anything_else
* ask_what_is_possible
    - utter_ask_what_is_possible
* out_of_scope
    - utter_out_of_scope

## story number 5
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
    - form{"name": null}
* thank
    - utter_no_worries
    - utter_anything_else
* out_of_scope
    - utter_out_of_scope

## story number 6
* greet
    - utter_greet
* ask_who_is_it
    - action_chitchat
* ask_what_is_possible
    - action_chitchat

## story number 7
* greet
    - utter_greet
* greet
    - utter_greet
* ask_who_is_it
    - action_chitchat


## story number 8
* greet
    - utter_greet
* enter_data
    - utter_not_sure
    - utter_ask_what_is_possible
* enter_data
    - utter_not_sure
    - utter_ask_what_is_possible

## story number 9
* greet
    - utter_greet
* enter_data
    - utter_not_sure
    - utter_ask_what_is_possible
* deny
    - utter_nohelp

## story number 11, continue
* greet
    - utter_greet
* ask_what_is_possible
    - action_chitchat
* ask_weather
    - action_chitchat
* ask_weather
    - action_chitchat
* ask_weather
    - action_chitchat
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
* deny
    - utter_cantsignup
    - utter_ask_continue_newsletter
* affirm
    - utter_great
    - subscribe_newsletter_form
    - form{"name": null}
    - utter_anything_else

## story number 11, don't continue
* greet
    - utter_greet
* ask_what_is_possible
    - action_chitchat
* ask_weather
    - action_chitchat
* ask_weather
    - action_chitchat
* ask_weather
    - action_chitchat
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
* deny
    - utter_cantsignup
    - utter_ask_continue_newsletter
* deny
    - utter_thumbsup
    - action_deactivate_form
    - form{"name": null}
    - utter_anything_else

## story number 12
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
    - form{"name": null}
    - utter_anything_else
* enter_data
    - utter_thumbsup
    - utter_anything_else

## story number 12, continue
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
* out_of_scope
    - utter_out_of_scope
    - utter_ask_continue_newsletter
* affirm
    - utter_great
    - subscribe_newsletter_form
    - form{"name": null}
    - utter_anything_else
* enter_data
    - utter_thumbsup
    - utter_anything_else

## story number 12, don't continue
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
* out_of_scope
    - utter_out_of_scope
    - utter_ask_continue_newsletter
* deny
    - utter_thumbsup
    - action_deactivate_form
    - form{"name": null}
    - utter_anything_else
* enter_data
    - utter_thumbsup
    - utter_anything_else

## story number 14
* greet
    - utter_greet
* greet
    - utter_greet
* ask_how_doing
    - action_chitchat
* ask_weather
    - action_chitchat

## story number 15
* greet
    - utter_greet
* ask_weather
    - action_chitchat
* enter_data
    - utter_not_sure
    - utter_ask_what_is_possible

## story number 17
* greet
    - utter_greet
* deny
    - utter_nohelp
* out_of_scope
    - utter_out_of_scope
    - utter_ask_what_is_possible
* ask_who_is_it
    - action_chitchat
* ask_how_doing
    - action_chitchat
* ask_how_doing
    - action_chitchat
* ask_what_is_possible
    - action_chitchat

## story number 18
* greet
    - utter_greet
* ask_weather
    - action_chitchat
* ask_what_is_possible
    - action_chitchat
* deny
    - utter_nohelp
* enter_data
    - utter_not_sure
    - utter_ask_what_is_possible
* deny
    - utter_nohelp
* out_of_scope
    - utter_out_of_scope
    - utter_ask_what_is_possible
* enter_data{"number":5}
    - utter_not_sure
    - utter_ask_what_is_possible
* enter_data
    - utter_not_sure
    - utter_ask_what_is_possible



## 
* greet
    - utter_greet
* greet
    - utter_greet
* ask_is_bot
    - action_chitchat
* affirm
    - utter_thumbsup

## 
* greet
    - utter_greet
* greet
    - utter_greet
* ask_how_doing
    - action_chitchat
* affirm
    - utter_thumbsup

## 
* greet
    - utter_greet
* enter_data
    - utter_not_sure
    - utter_ask_what_is_possible
* deny
    - utter_thumbsup
    - utter_anything_else
* affirm
    - utter_thumbsup

## 
* greet
    - utter_greet
* greet
    - utter_greet
* affirm
    - utter_thumbsup

## how doing
* ask_how_doing
    - action_chitchat
* ask_who_is_it
    - action_chitchat
* enter_data
    - utter_not_sure
    - utter_ask_what_is_possible

## 
* ask_who_am_i
    - action_chitchat
* ask_languages_bot
    - action_chitchat
* ask_how_old
    - action_chitchat
* out_of_scope{"number":42}
    - utter_out_of_scope
    - utter_ask_what_is_possible
* out_of_scope{"number":42}
    - utter_out_of_scope
    - utter_ask_what_is_possible
