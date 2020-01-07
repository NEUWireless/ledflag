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
        # Possible issue: if queries are dropped, the server may become out of sync with the worker,
        # as is expects are response for each query and is not guaranteed one
        self.query_queue = Queue(maxsize=max_queue_size)
        self.timeout = timeout

    def connect(self):
        self.connection = self.listener.accept()

    def listen(self):
        listen_process = Thread(target=self._listen_worker)
        listen_process.start()

    def begin_processing(self):
        # Thread for processing jobs
        job_process = Thread(target=self._job_worker)
        job_process.start()
        # Thread for processing queries
        query_process = Thread(target=self._query_worker)
        query_process.start()

    def _listen_worker(self):
        # Receive messages in a loop
        while True:
            try:
                msg = self.connection.recv()
                self.message_handler(msg)
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
            self.job_handler(job)

    def _query_worker(self):
        while True:
            query = self.query_queue.get()
            response = self.query_handler(query)
            self.connection.send(response)

    def message_handler(self, msg: Message):
        if isinstance(msg, Job):
            try:
                self.job_queue.put(msg, timeout=self.timeout)
            except Full:
                print("Job skipped, queue is full.")
        elif isinstance(msg, Query):
            try:
                self.query_queue.put(msg, timeout=self.timeout)
            except Full:
                print("Query skipped, queue is full.")
        else:
            raise Exception("A Message must be a Job or a Query")

    def free(self):
        return self.job_queue.empty()

    def start(self):
        self.connect()
        self.listen()
        self.begin_processing()
