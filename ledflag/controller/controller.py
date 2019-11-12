from ledflag.bridge.client import MessageClient
from ledflag.bridge.message import Message, DisplayText, DisplayScrollingText, DisplayImage
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from ledflag.controller.text import display_text, display_scrolling_text
from datetime import datetime
from queue import Queue, Full
from typing import Callable


msg_functions = {
    DisplayText: display_text,
    DisplayScrollingText: display_scrolling_text,
    DisplayImage: lambda msg, matrix: print("Displaying image...")
}


class LedController:

    def __init__(self):
        # Configure Matrix Options
        options = RGBMatrixOptions()
        options.rows = 32
        options.chain_length = 2
        options.parallel = 1
        options.hardware_mapping = 'adafruit-hat'
        self.matrix = RGBMatrix(options=options)
        self.message_queue = Queue(maxsize=10)

    def message_handler(self, msg: Message):
        """
        Handles each incoming message from the message server, calling the appropriate
        function for each message to update the LED matrix.

        :param msg: The message from the server
        :return: None
        """

        # Print a debug statement
        print("[{}] Received > {}".format(
            datetime.now().strftime("%I:%M%p"), msg)
        )

        try:
            self.message_queue.put(msg, timeout=5.0)
        except Full:
            print("Ignored message {} — Timeout occurred".format(msg))

    def run_msg(self, msg: Message, func: Callable, free=None):
        if not free:
            free = self.message_queue.empty
        func(msg, self.matrix, free=free)

    def start(self):
        mc = MessageClient()
        mc.listen(self.message_handler)
        while True:
            msg = self.message_queue.get()
            self.run_msg(msg, msg_functions[type(msg)])


if __name__ == '__main__':
    controller = LedController()
    controller.start()
