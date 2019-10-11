from multiprocessing.connection import Client, Process
from typing import Callable
from .config import Config
from .message import Message

class MessageClient:

    def __init__(self):
        self.connection = Client(Config.address)

    def listen(self, callback: Callable[[Message]]):
        listen_process = Process(target=self._listen_worker, args=(callback,))
        listen_process.start()

    def _listen_worker(self, callback: Callable[[Message]]):
        while True:
            msg = self.connection.recv()
            callback(msg)
