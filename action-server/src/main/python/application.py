import logging
import os
from typing import Dict
from dotenv import load_dotenv
import falcon
from falcon_cors import CORS
from rasa_sdk.executor import ActionExecutor
from rasa_sdk import ActionExecutionRejection
import version

load_dotenv()

REQUIRED_ENV_VARS = ()

OPTIONAL_ENV_VARS = ('CORS_ORIGINS',)

logger = logging.getLogger(__name__)


class InfoHandler:
    def on_get(self, req, resp):
        resp.media = {"component": "action server",
                      "version": version.__version__}


class ActionsHandler:
    def __init__(self, executor):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.executor = executor

    def on_post(self, req, resp):
        action_call = req.media
        try:
            resp.media = self.executor.run(action_call)
        except ActionExecutionRejection as e:
            self.logger.exception("action execution rejected")
            raise falcon.HTTPInternalServerError(
                f"action execution rejected {e.action_name}", str(e))

    def on_get(self, req, resp):
        actions = sorted(list(self.executor.actions.keys()))
        resp.media = {"actions": actions}


def load_environment_configuration():
    config = {k: os.getenv(k) for k in REQUIRED_ENV_VARS}
    for k, v in config.items():
        if v is None:
            raise ValueError("Missing configuration: "
                             f"environment variable '{k}' is not defined")

    for k in OPTIONAL_ENV_VARS:
        value = os.getenv(k)
        if value:
            config[k] = value

    return config


def create_app(config: Dict[str, str], executor: ActionExecutor):
    cors_origins = config.get('CORS_ORIGINS', '*').split(" ")
    if '*' in cors_origins:
        cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)
    else:
        cors = CORS(allow_origins_list=cors_origins, allow_all_headers=True, allow_all_methods=True)

    app = falcon.API(middleware=[cors.middleware, ])
    app.add_route('/info', InfoHandler())
    app.add_route('/webhook', ActionsHandler(executor))
    return app


config = load_environment_configuration()
executor = ActionExecutor()
executor.register_package('actions')
app = create_app(config, executor)
