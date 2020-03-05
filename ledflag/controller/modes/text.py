from time import sleep
from ledflag.controller.modes.mode import Args, Mode
from flask_socketio import SocketIO
from rgbmatrix import RGBMatrix, graphics
from os import path
from ledflag.definitions import PROJECT_ROOT

FONTS_DIR = path.join(PROJECT_ROOT, "controller/fonts")


class TextArgs(Args):
    """
    Arguments to TextMode.
    """
    def __init__(self, text: str, size: int):
        """
        :param text: The text to display on the LED Flag
        :param size: How large the text should be
        """
        super().__init__()
        self.text = text
        self.size = size


class TextMode(Mode):
    """
    Allows a user to display text that scrolls across the LED Flag.
    """
    def __init__(self, matrix: RGBMatrix, socketio: SocketIO):
        super().__init__(matrix, socketio)

    def run(self, args: TextArgs, **kwargs):
        """
        Displays and continually scrolls the text given by the TextArgs
        """
        free = kwargs['free']
        self.matrix.Clear()
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(path.join(FONTS_DIR, "7x13.bdf"))
        color = graphics.Color(76, 245, 141)
        pos = offscreen_canvas.width
        my_text = args.text

        while free():
            offscreen_canvas.Clear()
            text_length = graphics.DrawText(offscreen_canvas, font, pos, 19, color, my_text)
            pos -= 1
            if pos + text_length < 0:
                pos = offscreen_canvas.width
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            sleep(0.05)
