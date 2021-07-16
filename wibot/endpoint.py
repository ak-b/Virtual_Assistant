import json
import pyapp
import logging
import socket
from typing import List

import requests

from wibot.utils import get_config

from wibot import BOT_AUTH_HEADER

from wibot import BOT_NAME, BOT_AUTH_HEADER

#configs = get_config()

#BOT_NAME = configs['BOT_NAME']

BOT_NAME = 'awsm-o'

LOGGER = logging.getLogger(__name__)

SPARK_DEVICES_URL = "https://wdm-a.wbx2.com/wdm/api/v1/devices"

BOT_MODEL = "pyapp"
BOT_DEVICE_TYPE = "DESKTOP"
BOT_LOCALIZED_MODEL = "pyapp"
BOT_SYSTEM_NAME = "IaaS"
BOT_SYSTEM_VERSION = "0.0.1"


class SparkEndpoint:

    def __init__(self):
        self.hostname = socket.gethostname()

    def setup(self):
        LOGGER.debug('Setting up endpoint')
        self.delete_all_existing_devices()
        self.register_device()

    def register_device(self):
        existing_registered_devices = self.get_all_devices()
        devices = list(filter(lambda device: device['deviceIdentifier'] == self.hostname, existing_registered_devices))
        if devices:
            LOGGER.info("Device {} is already registered".format(self.hostname))
            return

        payload = {
            "DeviceCreateRequest": True,
            "deviceType": BOT_DEVICE_TYPE,
            "name": BOT_NAME,
            "model": BOT_MODEL,
            "localizedModel": BOT_LOCALIZED_MODEL,
            "systemName": BOT_SYSTEM_NAME,
            "systemVersion": BOT_SYSTEM_NAME,
            "deviceIdentifier": self.hostname,
            "isDeviceManaged": "false"
        }

        response = requests.request("POST", SPARK_DEVICES_URL, data=json.dumps(payload),
                                    headers=BOT_AUTH_HEADER)
        return response.json()

    def get_all_devices(self) -> List[str]:
        LOGGER.debug('Getting all devices')

        response = requests.get(SPARK_DEVICES_URL, headers=BOT_AUTH_HEADER)
        print(response.status_code)
        print(response)

        if response.status_code == 404:
            return list()

        data = response.json()
        if 'message' in data and 'No devices found' in data['message']:
            return list()

        return data['devices']

    def delete_all_existing_devices(self):
        LOGGER.debug('Deleting all existing endpoints')
        #print(self.get_all_devices())
        list(map(lambda device: requests.request("DELETE", device['url'], headers=BOT_AUTH_HEADER),
                 self.get_all_devices()))

    def get_websocket_url(self):
        devices = list(filter(lambda device: device['deviceIdentifier'] == self.hostname, self.get_all_devices()))
        return devices[0]['webSocketUrl'] + "/replicate" if devices else None
