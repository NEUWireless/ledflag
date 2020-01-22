from typing import TypeVar


class Message:

    def __init__(self):
        pass


class Job(Message):

    def __init__(self):
        super().__init__()


class Query(Message):

    def __init__(self, q: str):
        super().__init__()
        self.q = q


TJob = TypeVar('TJob', bound=Job)
TQuery = TypeVar('TQuery', bound=Query)
