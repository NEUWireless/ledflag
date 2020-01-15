from iotbridge.worker import Worker
from ledflag.bridge.message import Instruction, ModeQuery as Query
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from flask_socketio import SocketIO


class LedController:
    """
    The LED Flag controller is the object which handles instructions from the worker and displays
    the corresponding graphics on the LED matrix. It also responds to queries about its current state/mode.
    """
    def __init__(self):
        # Configure Matrix Options
        options = RGBMatrixOptions()
        options.rows = 32
        options.chain_length = 2
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat'
        # Create the matrix object
        self.matrix = RGBMatrix(options=options)
        # Initialize the worker
        self.worker = Worker(self.job_handler, self.query_handler)
        # Starts in undefined mode
        self.mode = None
        self.socketio = SocketIO(message_queue="redis://")

    def job_handler(self, job: Instruction):
        """
        Processes instructions from the web server.
        When a new instruction comes in, the mode is switched if necessary and the arguments
        are passed to the current mode.

        @param job: The instruction that tells the controller what to do (e.g. draw these three pixels)
        """
        # Switch the mode if a new mode is requested
        if not isinstance(self.mode, job.mode):
            self.mode = job.mode(self.matrix, self.socketio)
        # Execute the mode's run method
        self.mode.run(job.args, free=self.worker.free)

    def query_handler(self, query: Query):
        """
        Processes queries from the web server and responds appropriately.

        @param query: What information the web server needs from the controller
        """
        if not query.mode:
            # If the query does not specify a mode, it is a general query
            # e.g. what mode is the led flag currently in?
            return None
        if isinstance(self.mode, query.mode):
            # If the query is about the mode the flag is currently in,
            # have that mode handle the query
            return self.mode.handle_query(query.q)

    def start(self):
        """
        Starts the LED controller.
        """
        self.worker.start()


if __name__ == '__main__':
    controller = LedController()
    controller.start()
