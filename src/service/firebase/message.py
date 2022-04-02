import logging
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, messaging


class SendMessage:

    def __init__(self, topic, dir):
        logging.basicConfig(level=logging.DEBUG, filename= dir + datetime.now().date().__str__() + '.log',
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.topic = topic

    def send(self, title, msg , data):
        try:
            message = messaging.Message(
                data={
                    'title': title,
                    'msg': msg,
                    'time': str(data[0]),
                    'rain': str(data[1]),
                },
                topic=self.topic,
            )
            response = messaging.send(message)
            logging.debug("Successfully sent message: " + str(response))
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
