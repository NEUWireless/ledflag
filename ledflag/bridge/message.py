from iotbridge.message import Job, Query
from ledflag.controller.modes.mode import Mode, Args
from typing import Type, Optional


class Instruction(Job):
    """
    An instruction is sent by the web server to the controller in order
    to change or update the current mode.
    """
    def __init__(self, mode: Type[Mode], args: Args):
        """
        @param mode: The mode to be updated/swapped to
        @param args: The information necessary for the mode to be executed
        """
        super().__init__()
        self.mode = mode
        self.args = args


class ModeQuery(Query):
    """
    A ModeQuery is used to query the controller for information about its current mode
    """
    def __init__(self, mode: Optional[Type[Mode]], q: str):
        """
        @param mode: The mode to query information about (if no mode is specified,
        the query is assumed to be about general information such as "what mode is
        the led flag currently in?"
        @param q: The property/state to be queried (e.g. 'pixels' for the current state
        of the led flag's pixels)
        """
        super().__init__(q)
        self.mode = mode
