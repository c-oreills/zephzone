from json import load
import os

from pyfcm import FCMNotification
from slackclient import SlackClient

CONFIG_PATH = '~/.zephzone'
CONFIG_PATH = os.path.expanduser(CONFIG_PATH)
CONFIG = load(open(CONFIG_PATH))

DND_SECS = 60 * 60


def dnd_phone(config):
    if not config.get('ANDROID_API_KEY'):
        return

    push_service = FCMNotification(api_key=config["ANDROID_API_KEY"])

    registration_id = config["ANDROID_INSTANCE_ID"]

    data_message = {
        "action": "start_dnd",
        "dnd_secs": str(DND_SECS),
    }

    result = push_service.notify_single_device(
        registration_id=registration_id, data_message=data_message)


def dnd_slack(config):
    if not config.get('SLACK_API_TOKEN'):
        return

    sc = SlackClient(config['SLACK_API_TOKEN'])

    sc.api_call("dnd.setSnooze", num_minutes=DND_SECS / 60)


if __name__ == '__main__':
    dnd_phone(CONFIG)
    dnd_slack(CONFIG)
