import logging
from datetime import datetime

import firebase_admin
from firebase_admin import credentials

from growCare.Database.connection import Connection
from growCare.Device.data import Data

from os import listdir, remove
from os.path import isfile, join
from datetime import timedelta, datetime

FILENAME = '/home/pi/GrowCareProject/log/' + datetime.now().date().__str__()
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

directory = '/home/pi/GrowCareProject/log/'


def auto_remove_old_files():
    max_date = datetime.now() - timedelta(days=6)
    only_files = [f for f in listdir(directory) if isfile(join(directory, f))]
    for file_name in only_files:
        date_string = file_name.split('.')
        file_date = datetime.strptime(date_string[0], '%Y-%m-%d')
        if file_date <= max_date:
            remove('{}{}'.format(directory, file_name))


class DeviceHandler:

    def __init__(self, connection=None):
        self.connection = connection
        if self.connection is None:
            self.connection = Connection()
        self.devices = None

    def start(self):
        for device in self.connection.get_devices():
            data = Data(device.mac_address, device.id)
            data.start()
            self.devices.append(data)

    def restart_session(self):
        for device in self.devices:
            device.do_run = False
        self.devices = []
        for device in self.connection.get_devices():
            data = Data(device.mac_address, device.id)
            data.start()
            self.devices.append(data)


if __name__ == '__main__':
    try:
        auto_remove_old_files()
        logging.basicConfig(filename=FILENAME, format=FORMAT, level=logging.DEBUG, filemode='a')
        cred = credentials.Certificate(
            "/home/pi/GrowCareProject/weather-2df3e-firebase-adminsdk-ra7y9-d896f048b0.json")
        firebase_admin.initialize_app(cred)
        logging.info("Start script for growCare getter")
        device_handler = DeviceHandler()
        device_handler.start()
    except Exception as e:
        logging.error("An Exception occurred!", exc_info=True)