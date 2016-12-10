import argparse
from json import load
import os
import subprocess

from pyfcm import FCMNotification
from slackclient import SlackClient

CONFIG_PATH = '~/.zephzone'
CONFIG_PATH = os.path.expanduser(CONFIG_PATH)
CONFIG = load(open(CONFIG_PATH))

DND_SECS = 60 * 60


def dnd_phone(config, unset=False):
    if not config.get('ANDROID_API_KEY'):
        return

    push_service = FCMNotification(api_key=config["ANDROID_API_KEY"])

    registration_id = config["ANDROID_INSTANCE_ID"]

    if unset:
        data_message = {
            "action": "stop_dnd",
        }
    else:
        data_message = {
            "action": "start_dnd",
            "dnd_secs": str(DND_SECS),
        }

    result = push_service.notify_single_device(
        registration_id=registration_id, data_message=data_message)


def dnd_slack(config, unset=False):
    if not config.get('SLACK_API_TOKEN'):
        return

    sc = SlackClient(config['SLACK_API_TOKEN'])

    if unset:
        sc.api_call("dnd.endSnooze")
    else:
        sc.api_call("dnd.setSnooze", num_minutes=DND_SECS / 60)


def open_brain_fm_focus(config, unset=False):
    if unset or not config.get('BRAIN_FM'):
        return

    devnull = open(os.devnull, 'w')

    subprocess.call(['gnome-open', 'https://www.brain.fm/app#!/player/35'], stdout=devnull, stderr=subprocess.STDOUT)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--unset', nargs='?', const=True, default=False)

    args = parser.parse_args()

    dnd_phone(CONFIG, unset=args.unset)
    dnd_slack(CONFIG, unset=args.unset)
    open_brain_fm_focus(CONFIG)
