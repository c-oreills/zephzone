from json import load

from pyfcm import FCMNotification


config = load(open('~/.zephzone'))

push_service = FCMNotification(api_key=config["ANDROID_API_KEY"])

registration_id = config["ANDROID_INSTANCE_ID"]

data_message = {
    "action" : "start_dnd",
    "dnd_secs" : "3600",
}

result = push_service.notify_single_device(registration_id=registration_id, data_message=data_message)
