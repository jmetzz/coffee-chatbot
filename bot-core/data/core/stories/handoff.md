## chitchat
* human_handoff
    - utter_contact_email

## greet + handoff
* greet
    - utter_greet
* human_handoff
    - utter_contact_email

## just newsletter + handoff, continue
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
* human_handoff
    - utter_contact_email
    - utter_ask_continue_newsletter
* affirm
    - utter_great
    - subscribe_newsletter_form
    - form{"name": null}
    - utter_anything_else
* bye
    - utter_bye

## just newsletter + handoff, don't continue
* greet
    - utter_greet
* signup_newsletter
    - utter_can_do
    - subscribe_newsletter_form
    - form{"name": "subscribe_newsletter_form"}
* human_handoff
    - utter_contact_email
    - utter_ask_continue_newsletter
* deny
    - utter_thumbsup
    - action_deactivate_form
    - form{"name": null}
    - utter_anything_else


