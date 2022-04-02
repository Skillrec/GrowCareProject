import argparse
import logging
from datetime import datetime
from threading import Thread

from btlewrap import BluepyBackend
from miflora import miflora_scanner
import bluepy

from growCare.Database.connection import Connection
from src.model.device import Device

import os


FILENAME = os.path.expanduser(
    '~') + 'GrowCareProject/log/scanner/' + str(datetime.now().date())
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=FILENAME, format=FORMAT,
                    level=logging.DEBUG, filemode='a')


def search_bl_devices():
    """Scan for sensors."""
    devices_founded = []
    backend = BluepyBackend
    devices_mi = miflora_scanner.scan(backend, 12)
    logging.info('{} Devices found'.format(len(devices_mi)))
    for device in devices_mi:
        logging.info('{}'.format(device))
        devices_founded.append(Device(0, '', device))
    return devices_founded


def check_device(mac_address):
    con = Connection()
    check = True
    for device in con.get_devices():
        if device.mac_address == mac_address:
            check = False
    return check


def add_new_device(mac_address):
    con = Connection()
    con.add_new_device(("New Device", mac_address))
    logging.info("New Device is added.")
