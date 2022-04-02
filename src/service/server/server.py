import logging
import socket
import json
from collections import namedtuple
from threading import Thread

from growCare.Device.data import Data
from growCare.Device.scanner import search_bl_devices, check_device, add_new_device
from growCare.Server.package import Package


def custom_package_decoder(package_dict):
    return namedtuple('X', package_dict.keys())(*package_dict.values())


class Server(Thread):

    def __init__(self,device_handler, port=64532, host=''):
        super(Server, self).__init__()
        self.port = port
        self. host = host
        self.device_handler = device_handler
        self.pack = None
        self.devices_found = []
        self.devices = None

    def run(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                self.pack = None
                conn, address = s.accept()
                with conn:
                    print("Connected by: ", address)
                    while True:
                        data = conn.recv(1024)
                        print("Received data: ", data)
                        self.pack = json.loads(data, object_hook=custom_package_decoder)
                        self.handle_request(conn)
                        print("Get Package: ", self.pack.device)
                        if not data:
                            break
                        print("Send it back")
                        conn.sendall(data)

    def handle_request(self,  conn):
        if self.pack.requestCode == 1:
            self.restart_code()
        elif self.pack.requestCode == 2:
            num_dev = self.scan()
            package = Package(response=str(num_dev), errorCode=0, requestCode=2)
            conn.sendall(json.dumps(package))

    def restart_code(self):
        self.device_handler.restart_session()

    def scan(self):
        self.devices = search_bl_devices()
        if self.devices is not []:
            for device in self.devices:
                if check_device(device.mac_address):
                    logging.info("New Device found")
                    self.devices_found.append(device)
                    add_new_device(device.mac_address)
                    self.device_handler.restart_session()
            return len(self.devices_found)




