import logging
from datetime import datetime
import time
import importlib
import json

from src.model.device import Device
from uuid import getnode as get_mac


FILENAME = '/home/pi/GrowCareProject/log/' + datetime.now().date().__str__()
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'


@staticmethod
def get_mac_address():
    return get_mac()


@staticmethod
def check_module(module):
    module_loader = importlib.find_loader(module)
    if module_loader is not None:
        from mysql import connector as mc
    return module_loader is not None


class Connection:

    def __init__(self):
        logging.basicConfig(filename=FILENAME, format=FORMAT,
                            level=logging.DEBUG, filemode='a')
        logging.info("Connection: Initializing the class")
        self.config = "../../config/main.config.json"
        self.load_config()

        self.connection = None
        self.cursor = None

    def load_config(self):
        with open(self.config) as config_file:
            data = json.load(config_file)
            self.ip = data['server']['ip']
            self.user = data['server']['user']
            self.pwd = data['server']['password']
            self.db = data['server']['db_name']
            self.module = data['module']

    def connect(self):
        if check_module(self.module):
            try:
                self.connection = mc.connect(host=self.ip,
                                             user=self.user,
                                             password=self.password,
                                             db=self.db)
                self.cursor = self.connection.cursor()
            except Exception as e:
                logging.error("An Exception occurred", exc_info=True)

    def add_new_device(self, args):
        self.connect()
        query = "INSERT INTO Grow_Care_Device (NAME, MAC_ADDRESS, IDGrow_Care_distributor) VALUES (%s, %s,  " \
                "(Select IDGrow_Care_distributor From Grow_Care_distributor Where MAC_ADDRESS = %s)) "
        args += (str(get_mac_address()),)
        self.cursor.execute(query, args)
        self.connection.commit()

    def insert_data(self, id_device, args):
        try:
            self.connect()
            val = tuple(args) + (str(id_device),)
            logging.info("Write data {} into db".format(str(val)))
            query = 'INSERT INTO Grow_Care_History (SOIL_MOISTURE, SOIL_FERTILITY, LIGHT, TEMPERATURE, ' \
                    'BATTERY, IDGrow_Care_Device) VALUE (%s, %s, %s, %s, %s, %s) '
            self.cursor.execute(query, val)
            self.connection.commit()
            self.update_last_sync(id_device, last_sync=time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime()))
        except Exception as e:
            logging.error("An Exception occurred", exc_info=True)

    def get_devices(self):
        try:
            self.connect()
            mac = get_mac_address()
            logging.info('MAC-ADDRESS of the raspberry {}'.format(mac))
            query = 'SELECT IDGrow_Care_distributor FROM Grow_Care_distributor WHERE MAC_ADDRESS = %s'
            self.cursor.execute(query, (mac,))
            id = self.cursor.fetchall()
            if id is not []:
                id_ = id[0][0]
                query = "SELECT IDGrow_Care_Device, NAME, MAC_ADDRESS FROM Grow_Care_Device WHERE " \
                        "IDGrow_Care_distributor = %s "
                self.cursor.execute(query, (str(id_),))
                set = self.cursor.fetchall()
                devices = []
                for id, name, address in set:
                    device = Device(id, name, address)
                    devices.append(device)
                return devices
        except Exception as e:
            logging.error('An Exception occurred!', exc_info=True)
        return None

    def update_device_name(self, id_device, device_name):
        self.connect()
        query = 'UPDATE Grow_Care_Device SET NAME = %s WHERE IDGrow_Care_Device = %s'
        self.cursor.execute(query, (device_name, str(id_device)))
        self.connection.commit()

    def update_last_sync(self, id_device, last_sync):
        self.connect()
        query = "UPDATE Grow_Care_Device SET LastSync = %s WHERE IDGrow_Care_Device = %s"
        self.cursor.execute(query, (last_sync, id_device))
        self.connection.commit()
