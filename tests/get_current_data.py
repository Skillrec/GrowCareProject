import logging
import sys

from growCare.Database.connection import Connection
from growCare.Device.data import Data

if __name__ == '__main__':
    logging.info("Start script for growCare getter")
    connection = Connection()
    id_device = 0
    if sys.argv[1] is not None:
        id_device = int(sys.argv[1])
    for device in connection.get_devices():
        if device.get_id() == id_device:
            data = Data(device.mac_address, device.id, True)
            data.start()