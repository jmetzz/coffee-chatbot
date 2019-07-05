from .actions import ActionSimpleTextForm

VERSION_FORM_ALLOWED_ANSWERS = {"extra": ["extra"],
                                "bestaande": ["bestaande", "vervangen"]}

APP_FORM_ALLOWED_ANSWERS = {'mobile': ["mobile"],
                            'touch': ["touch"],
                            'sign': ["sign"],
                            'itsme': ["itsme"]}

CODE_FORM_ALLOWED_ANSWERS = {'app code': ["app code", "vijfcijferige code", "vijfcijferige", "app"],
                             'pin': ["pin", "viercijferige code", "kaart", "kaartcode", "kaartpin"]}

REFUND_TYPE_FORM_ALLOWED_ANSWERS = {"persoonlijk": ["persoonlijk", "eigen", "zelf"],
                                    "shop": ["shop", "winkel", "handelaar"],
                                    "webshop": ["webshop", "internet", "online"]}

AppForm = type("AppForm",
               (ActionSimpleTextForm,),
               {"inform_slot": "app",
                "action_name": "app_form",
                "allowed_answers": APP_FORM_ALLOWED_ANSWERS})

CodeForm = type("CodeForm",
                (ActionSimpleTextForm,),
                {"inform_slot": "identification",
                 "action_name": "code_form",
                 "allowed_answers": CODE_FORM_ALLOWED_ANSWERS})

RefundTypeForm = type("RefundTypeForm",
                      (ActionSimpleTextForm,),
                      {"inform_slot": "channel-non-kbc",
                       "action_name": "refund_type_form",
                       "allowed_answers": REFUND_TYPE_FORM_ALLOWED_ANSWERS,
                       "utter_ask": "utter_refund_type"})
