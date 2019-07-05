## chitchat
* out_of_scope
    - utter_out_of_scope
    - utter_possibilities

## say enter data outside the flows
* greet
    - utter_greet
* enter_data
    - utter_not_sure
    - utter_possibilities

## say confirm outside the flows 2
* greet
    - utter_greet
* affirm
    - utter_thumbsup

## say greet outside the flows
* greet
    - utter_greet
* greet OR enter_data{"name": "akela"}
    - utter_greet

## just newsletter + confirm
* greet
    - utter_greet
* out_of_scope
    - utter_out_of_scope
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
    - form{"name": null}
    - utter_anything_else
* affirm
    - utter_thumbsup

## just newsletter, continue + confirm
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
* affirm
    - utter_thumbsup
    - utter_anything_else

## just newsletter, don't continue + confirm
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
* affirm
    - utter_thumbsup
    - utter_anything_else

## just newsletter (with email already) + confirm
* greet
    - utter_greet
* out_of_scope
    - utter_out_of_scope
* signup_newsletter{"email": "maxmeier@firma.de"}
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
    - form{"name": null}
* affirm
    - utter_thumbsup
    - utter_anything_else

## just newsletter (with email already)
* greet
    - utter_greet
* out_of_scope
    - utter_out_of_scope
* signup_newsletter{"email": "maxmeier@firma.de"}
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
    - form{"name": null}


## just newsletter
* greet
    - utter_greet
* out_of_scope
    - utter_out_of_scope
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
    - form{"name": null}

## just newsletter, continue
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


## just newsletter, don't continue
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

