from iotbridge.worker import Worker
from iotbridge.message import Job, Query
from ledflag.bridge.message import Instruction
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from flask_socketio import SocketIO


class LedController:

    def __init__(self):
        # Configure Matrix Options
        options = RGBMatrixOptions()
        options.rows = 32
        options.chain_length = 2
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat'
        self.matrix = RGBMatrix(options=options)
        self.worker = Worker(self.job_handler, self.query_handler)
        self.mode = None
        self.socketio = SocketIO(message_queue="redis://")

    def job_handler(self, job: Instruction, free=False):
        if not isinstance(self.mode, job.mode):
            self.mode = job.mode(self.matrix, self.socketio)
        self.mode.run(job.args, free=self.worker.free)

    def query_handler(self, query: Query):
        print(query)
        if query.q == "pixels":
            return self.mode.pixels
        return None

    def start(self):
        self.worker.start()


if __name__ == '__main__':
    controller = LedController()
    controller.start()
