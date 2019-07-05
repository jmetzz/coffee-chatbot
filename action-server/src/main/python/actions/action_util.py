import logging

import requests
from rasa_sdk.events import SlotSet
from rasa_sdk import Tracker

from typing import List, Tuple, Sequence


class ActionUtil:

    @staticmethod
    def call_service(class_name: str, tracker: Tracker, url: str) -> Tuple[bool, str, List[SlotSet]]:
        logger = logging.getLogger(class_name)

        headers = {'Content-type': 'application/json',
                   'sessionId': tracker.sender_id}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logger.error(f"call to {url} did not responded with 200. "
                         f"HTTPClientError message: {response.text}")

            return False, '', [SlotSet('action_success', False),
                               SlotSet('action_message', f" Unable to execute {class_name} "
                               f"HTTPClientError message: {response.text}")]

        data = response.json()

        if data['result'] == 'ERROR':
            logger.error(f" {url} returned ERROR with bood-kd {data['boodKdValue']}")

            return False, '', [SlotSet('action_success', False),
                               SlotSet('action_message', f"Unable to execute {class_name} "
                               f"with bood-kd {data['boodKdValue']} HTTPClientError message: {response.text}")]

        elif data['result'] == 'WARNING':
            logger.error(f" {url} returned WARNING with bood-kd {data['boodKdValue']}")

        return True, data, []

    @staticmethod
    def check_required_slots(class_name: str, slots: Sequence[str], tracker) -> Tuple[bool, List[SlotSet]]:
        for slot in slots:
            if tracker.get_slot(slot) is None:
                logging.getLogger(class_name).error(f"These slots cannot be None, {slots}")
                return False, [SlotSet('action_success', False),
                               SlotSet('action_message', f"These slots cannot be None, {slots}")]

        return True, []
