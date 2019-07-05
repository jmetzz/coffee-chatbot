import logging

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction, REQUESTED_SLOT

from typing import Text, Dict, Any, List

from fuzzywuzzy import process as proc
from fuzzywuzzy.fuzz import token_set_ratio

from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    FollowupAction,
    Form,
)

logger = logging.getLogger(__name__)


class SubscribeNewsletterForm(FormAction):
    """Asks for the user's email, call the newsletter API and sign up user"""

    def name(self):
        return "subscribe_newsletter_form"

    @staticmethod
    def required_slots(tracker):
        return ["email"]

    def slot_mappings(self):
        return {
            "email": [
                self.from_entity(entity="email"),
                self.from_text(intent="enter_data"),
            ]
        }

    def validate_email(self, value, dispatcher, tracker, domain):
        """Check to see if an email entity was actually picked up by duckling."""
        if any(tracker.get_latest_entity_values("email")):
            # entity was picked up, validate slot
            return {"email": value}
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_template("utter_no_email", tracker)
            return {"email": None}

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Once we have an email, attempt to add it to the database"""

        email = tracker.get_slot("email")
        logger.debug(email)
        # client = MailChimpAPI(config.mailchimp_api_key)
        # if the email is already subscribed, this returns False
        # added_to_list = client.subscribe_user(config.mailchimp_list, email)

        # utter submit template
        # if added_to_list:
        #    dispatcher.utter_template("utter_confirmation_email", tracker)
        # else:
        dispatcher.utter_template("utter_confirmation_email", tracker, **tracker.slots)
        return []


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List["Event"]:

        # Fallback caused by TwoStageFallbackPolicy
        if (
                len(tracker.events) >= 4
                and tracker.events[-4].get("name") == "action_default_ask_affirmation"
        ):

            dispatcher.utter_template("utter_restart_with_button", tracker)

            return [SlotSet("feedback_value", "negative"), ConversationPaused()]

        # Fallback caused by Core
        else:
            dispatcher.utter_template("utter_default", tracker)
            return [UserUtteranceReverted()]


class ActionChitchat(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self):
        return "action_chitchat"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")

        # retrieve the correct chitchat utterance dependent on the intent
        if intent in [
            "ask_how_to_brew",
            "ask_how_doing",
            "ask_how_old",
            "ask_is_bot",
            "ask_languages_bot",
            "ask_espresso_bar",
            "ask_time",
            "ask_weather",
            "ask_whatis",
            "ask_what_is_my_name",
            "ask_what_is_possible",
            "ask_where_from",
            "ask_who_am_i",
            "ask_who_is_it",
            "handle_insult",
            "ask_for_the_blog",
            "compliment",
            "ask_location",
            "ask_for_social_network",
            "ask_culture",
        ]:
            dispatcher.utter_template("utter_" + intent, tracker, **tracker.slots)
        return []


class ActionComposedUtter(Action):
    """A mixin class that can be used to easily instantiate actions in Rasa that consist
    of consecutive utters.

    Attributes:
        action_name: unique name that identifies the action in Rasa
        utter_list: template names, to be uttered in this order when action is called
    """

    action_name = "action_composed_utter"
    utter_list = None

    def name(self):
        return self.action_name

    def run(self, dispatcher, tracker, domain):
        for utter in self.utter_list:
            dispatcher.utter_template(utter, tracker)
        return []

    def __str__(self):
        return "UtterAction('{}')".format(self.name())

ActionScheduleAppointment = type("ActionScheduleAppointment",
                             (ActionComposedUtter,),
                             {"utter_list": ["utter_schedule_appointment", "utter_appointment_page"],
                              "action_name": "action_schedule_appointment"})


class ActionSimpleTextForm(FormAction):
    """A mixin class that can be used to easily instantiate basic form actions in Rasa. The scope
    of these form actions is limited to those that require only one slot to be filled and the way
    to extract it is solely via the text, no entities extracted or intents recognised by Rasa NLU
    are taken into account. The customer's answer is supposed to belong to a fixed lists of options
    and is matched against them with a fuzzy matching. The form starts by asking a question that
    needs to be specified in the domain under the fixed name "utter_ask_ + inform_slot". If the slot
    is not filled, the question is repeated once. After a second failure, the form is terminated.
    The bot's next action in both cases (successful slot filling or not) needs to be specified in
    additional stories.

    Attributes:
        action_name: unique name that identifies the action in Rasa
        inform_slot: the one (categorical) slot that needs to be filled by the form
        allowed_answers: a dictionary of options that the client can answer, keys are the (categorical) levels of the
        slot, the list of values are matched to the input to decide how to fill the slot
        _match_threshold: the threshold for fuzzy matching. The higher it is, the more the client's
                         input needs to match one of the option in allowed_answers
        _max_count: the maximum number the question needs to be asked before prematurely ending the form
    """
    action_name = "simple_text_form_action"
    inform_slot = None
    allowed_answers = None
    utter_ask = None
    _match_threshold = 80
    _max_count = 2

    _error_message = "Failed to validate slot {0} with action {1}"
    _counter_slot = "form_action_counter"

    def __init__(self):
        if self.utter_ask is None:
            self.utter_ask = "utter_ask_{}".format(str(self.inform_slot))

    def name(self):
        return self.action_name

    def required_slots(self, tracker):
        return [self.inform_slot]

    def slot_mappings(self):
        return {self.inform_slot: [self.from_text()]}

    def validate_slots(self, slot_dict, dispatcher, tracker, domain):
        events = []
        if self.inform_slot in slot_dict.keys():
            slot_value = slot_dict[self.inform_slot]
            new_slot_value = self._validate_candidate_slot_values(slot_value)
            events.extend([SlotSet(self.inform_slot, new_slot_value)])
        return events

    def _validate_candidate_slot_values(self, slot_value):
        best_match = None
        best_score = 0
        for allowed_answer, options in self.allowed_answers.items():
            _, highest_score = proc.extractOne(slot_value, options, scorer=token_set_ratio)
            if highest_score >= best_score:
                if highest_score == best_score:
                    best_match = None
                else:
                    best_match = allowed_answer
                best_score = highest_score
        return best_match if best_score >= self._match_threshold else None

    def request_next_slot(self, dispatcher, tracker, domain):
        counter = tracker.get_slot(self._counter_slot)
        if counter < self._max_count and self._should_request_slot(tracker, self.inform_slot):
            dispatcher.utter_template(self.utter_ask, tracker, silent_fail=False,
                                      **tracker.slots)
            return [SlotSet(REQUESTED_SLOT, self.inform_slot), SlotSet(self._counter_slot, counter + 1)]
        return None

    def submit(self, dispatcher, tracker, domain):
        return [SlotSet(self._counter_slot, 0)]


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
