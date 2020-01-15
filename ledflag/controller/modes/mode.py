from rgbmatrix import RGBMatrix
from flask_socketio import SocketIO
from typing import Any


class Args:
    """
    Represents the arguments to a mode,
    such as the text and font size arguments to DrawMode
    """
    def __init__(self):
        pass


class Mode:
    """
    A mode that the LED Flag can be in, which handles exactly one type of functionality
    For example, drawing on the screen or displaying scrolling text
    """
    def __init__(self, matrix: RGBMatrix, socketio: SocketIO):
        self.matrix = matrix
        self.socketio = socketio

    def run(self, args: Args, **kwargs):
        """
        Starts or updates the mode with the arguments provided. This is where the main logic of the mode goes.

        @param args: The information needed to run (or update) the mode
        @param kwargs: Contains the "free" function, which returns true only while there is no other
        message waiting in the queue (e.g. if a draw command is waiting for scrolling text to finish, free will
        return false)
        """
        pass

    def handle_query(self, query: str) -> Any:
        """
        Responds to a given query about the mode, such as the state of the pixels in DrawMode

        @param query: What the query is asking for (e.g. 'pixels')
        """
        pass
