from iotbridge.message import Job
from ledflag.controller.mode import *
from typing import Type, Dict


class Instruction(Job):

    def __init__(self, mode: Type[Mode], args: Dict):
        super().__init__()
        self.mode = mode
        self.args = args
