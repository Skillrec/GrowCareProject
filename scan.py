import logging

from main import FILENAME, FORMAT

from growCare.Database.connection import Connection
from growCare.Device.data import Data
from growCare.Device.scanner import search_bl_devices, check_device, add_new_device

logging.basicConfig(filename=FILENAME, format=FORMAT, level=logging.DEBUG, filemode='a')


if __name__ == '__main__':
    try:
        devices_founded = []
        devices = search_bl_devices()
        if devices is not []:
            for device in devices:
                if check_device(device.mac_address):
                    logging.info("New Device found")
                    devices_founded.append(device)
                    add_new_device(device.mac_address)
                    connection = Connection()
                    for device_ in connection.get_devices():
                        if device_.mac_address == device.mac_address:
                            data = Data(device_.mac_address, device_.id)
                            data.start()
            print('{} Geräte gefunden'.format(len(devices_founded)))
        else:
            logging.info("No new Device founded")
    except Exception as e:
        logging.error('An Exception occurred!', exc_info=True)