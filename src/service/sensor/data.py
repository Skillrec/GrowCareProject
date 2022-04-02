import logging
from datetime import datetime
from threading import Thread
from time import sleep
import bluepy

from btlewrap.bluepy import BluepyBackend
from miflora.miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY

from growCare.Database.connection import Connection

FILENAME = '/home/pi/GrowCareProject/log/' + datetime.now().date().__str__()
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'


class Data(Thread):

    def __init__(self, mac_address, id, loop=False):
        logging.basicConfig(filename=FILENAME, format=FORMAT,
                            level=logging.DEBUG, filemode='a')
        Thread.__init__(self)
        self.mac_address = mac_address
        self.id = id
        self.loop = loop
        self.do_run = True
        logging.info(
            "Start selecting data for device with MAC-Address: {0} and ID: {1} ".format(self.mac_address, str(self.id)))

    def run(self):
        try:
            while self.do_run:
                self.insert_in_db()
                if self.loop:
                    print("success")
                    break
                sleep(1800)
        except Exception as e:
            logging.error("An Exception occurred", exc_info=True)

    def get_data(self):
        try:
            poller = MiFloraPoller(str(self.mac_address), BluepyBackend)
            return poller.parameter_value(MI_MOISTURE), poller.parameter_value(MI_CONDUCTIVITY), \
                poller.parameter_value(MI_LIGHT), poller.parameter_value(MI_TEMPERATURE), poller.parameter_value(
                MI_BATTERY)
        except bluepy.btle.BTLEDisconnectError as e:
            logging.error(
                "Can't connect and fetch the data from the device", exc_info=True)
        except Exception as e:
            logging.error("An Exception occurred", exc_info=True)

    def insert_in_db(self):
        try:
            connection = Connection()
            connection.insert_data(self.id, self.get_data())
        except TypeError as type_error:
            return False
