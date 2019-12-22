from multiprocessing.connection import Listener
from queue import Queue, Full
from threading import Thread
from typing import Callable
from .message import *
from .config import Config


class Worker:

    def __init__(self, job_handler: Callable, query_handler: Callable,
                 max_queue_size=50, timeout=5):
        self.job_handler = job_handler
        self.query_handler = query_handler
        self.listener = Listener(Config.address)
        self.connection = None
        self.job_queue = Queue(maxsize=max_queue_size)
        self.timeout = timeout

    def connect(self):
        self.connection = self.listener.accept()

    def listen(self):
        listen_process = Thread(target=self._listen_worker)
        listen_process.start()

    def _listen_worker(self):
        # Receive messages in a loop
        while True:
            try:
                msg = self.connection.recv()
                response = self.message_handler(msg)
                if response:
                    self.connection.send(response)
            # Catch the error caused by the connection closing
            except EOFError:
                return
            # Allow the user to exit with Ctrl+C
            except KeyboardInterrupt:
                print("Exiting...")
                return

    def _job_worker(self):
        while True:
            job = self.job_queue.get()
            self.job_handler(job, free=self.job_queue.empty)

    def message_handler(self, msg: Message):
        if isinstance(msg, Job):
            try:
                self.job_queue.put(msg, timeout=self.timeout)
            except Full:
                print("Job skipped, queue is full.")
            return None
        else:
            return self.query_handler(msg)

    def free(self):
        return self.job_queue.empty()

    def start(self):
        self.connect()
        self.listen()
        self._job_worker()
