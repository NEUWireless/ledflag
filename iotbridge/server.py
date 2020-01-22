from multiprocessing.connection import Client
from time import sleep
from .message import Job, Query
from .config import Config


class Server:

    def __init__(self):
        self.connection = None

    def connect(self):
        """
        Establishes a connection to the worker.
        """
        while not self.connection:
            try:
                self.connection = Client(Config.address)
            except ConnectionRefusedError:
                print("Connection refused. Retrying in 1 second...")
            sleep(1)
        print("Connection established!")

    def task(self, job: Job):
        """
        Send a job to the worker.
        """
        self.connection.send(job)

    def query(self, query: Query):
        """
        Query the worker for a value.
        """
        self.connection.send(query)
        try:
            return self.connection.recv()
        except BlockingIOError:
            print("Query not available")
            return None
