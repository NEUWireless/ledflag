from multiprocessing.connection import Listener
from .config import Config
from .message import Message


class MessageServer:

    def __init__(self):
        self.listener = Listener(Config.address)
        self.connection = None

    def connect(self):
        self.connection = self.listener.accept()

    def send(self, message: Message):
        self.connection.send(message)

    def close(self):
        self.connection.close()
