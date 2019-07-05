## kosten kaart via soort anything else 11
* costs{"bank_object": "kaart"}
    - soort_kaart_form
    - form{"name": "soort_kaart_form"}
    - slot{"requested_slot": "soort_kaart"}
    - slot{"soort_kaart": "V"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_utter_card_costs
* INFORM_Kaarten{"soort_kaart": "ALL"}
    - action_utter_card_costs

## soorten kaart via utter soort naar kredietkaart silver
* info{"bank_object": "kaart"}
    - utter_soort_kaart
* INFORM_Kaarten{"soort_kaart": "ALL"}
    - action_utter_card_info

