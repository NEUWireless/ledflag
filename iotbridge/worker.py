from multiprocessing.connection import Listener
from queue import Queue, Full
from threading import Thread
from typing import Callable, Any
from time import sleep
from .message import *
from .config import Config


class Worker:

    def __init__(self, job_handler: Callable[[TJob], None], query_handler: Callable[[TQuery], Any],
                 max_queue_size=50, timeout=5):
        """
        @param job_handler: The callback for when a new job is received
        @param query_handler: The callback for when a new query is received
        @param max_queue_size: The maximum number of instructions in the queue before the next one is dropped
        @param timeout: The amount of time to wait to place a job/query on the queue before dropping it (if full)
        """
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
        """
        Wait for a connection from the server.
        """
        print("Waiting for server...")
        self.connection = self.listener.accept()
        print("Connected!")

    def listen(self):
        """
        Start the listen worker.
        """
        listen_process = Thread(target=self._listen_worker)
        listen_process.start()

    def begin_processing(self):
        """
        Start the job and query workers.
        """
        # Thread for processing jobs
        job_process = Thread(target=self._job_worker)
        job_process.start()
        # Thread for processing queries
        query_process = Thread(target=self._query_worker)
        query_process.start()
        print("Job and Query processors started.")

    def _listen_worker(self):
        """
        Receive messages over the multiprocessing connection and add them to the corresponding queue,
        re-establishing the connection as necessary.
        """
        # Receive messages in a loop
        while True:
            try:
                msg = self.connection.recv()
                self.message_handler(msg)
            # Catch the error caused by the connection closing
            except (ConnectionResetError, EOFError):
                print("Connection dropped.")
                print("Retrying in 5 seconds...")
                sleep(5)
                self.connect()
                continue
            # Allow the user to exit with Ctrl+C
            except KeyboardInterrupt:
                print("Exiting...")
                return

    def _job_worker(self):
        """
        Continually pulls jobs from the queue and passes them to the job handler.
        """
        while True:
            job = self.job_queue.get()
            self.job_handler(job)

    def _query_worker(self):
        """
        Continually pulls queries from the queue and sends the response from the query handler
        """
        while True:
            query = self.query_queue.get()
            response = self.query_handler(query)
            self.connection.send(response)

    def message_handler(self, msg: Message):
        """
        Places a message on its respective queue.
        """
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

    def free(self) -> bool:
        """
        Indicates whether there are no waiting jobs (i.e. the worker is 'free')
        """
        return self.job_queue.empty()

    def start(self):
        """
        Starts the worker.
        """
        print("Starting worker...")
        self.connect()
        self.listen()
        self.begin_processing()
        print("Worker started.")
