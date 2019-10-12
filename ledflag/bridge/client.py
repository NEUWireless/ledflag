from multiprocessing import Process
from multiprocessing.connection import Client
from typing import Callable, Any
from .config import Config
from .message import Message


class MessageClient:

    def __init__(self):
        self.connection = Client(Config.address)

    def listen(self, callback: Callable[[Message], Any]):
        listen_process = Process(target=self._listen_worker, args=(callback,))
        listen_process.start()

    def _listen_worker(self, callback: Callable[[Message], Any]):
        while True:
            try:
                msg = self.connection.recv()
                callback(msg)
            except EOFError:
                return
