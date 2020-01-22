from typing import List, Dict, Any
from ledflag.controller.modes.mode import Args, Mode
from flask_socketio import SocketIO
from rgbmatrix import RGBMatrix


class DrawArgs(Args):
    """
    Arguments to DrawMode.
    """
    def __init__(self, pixels: List[Dict[str, int]]):
        """
        :param pixels: The pixels to draw to the led board. Takes the following format:
        [{x: int, y: int, r: int, g: int, b: int}]
        """
        super().__init__()
        self.pixels = pixels


class DrawMode(Mode):
    """
    Allows users to draw on the LED Flag.
    """
    def __init__(self, matrix: RGBMatrix, socketio: SocketIO):
        super().__init__(matrix, socketio)
        # The state of the LED Flag's pixels as a list of colors in the format [(r: int, g: int, b: int), ...]
        self.pixels = [(0, 0, 0)] * (matrix.width * matrix.height)
        self.matrix.Fill(0, 0, 0)

    def run(self, args: DrawArgs, **kwargs):
        """
        Draws the set of pixels given by DrawArgs on the LED Flag.
        """
        if len(args.pixels) == 0:
            self.pixels = [(0, 0, 0)] * (self.matrix.width * self.matrix.height)
            self.matrix.Fill(0, 0, 0)
            self.socketio.emit('draw_clear', {})
        else:
            for pixel in args.pixels:
                self.pixels[pixel['y'] * self.matrix.width + pixel['x']] = (pixel['r'], pixel['g'], pixel['b'])
                self.matrix.SetPixel(pixel['x'], pixel['y'], pixel['r'], pixel['g'], pixel['b'])
            self.socketio.emit('draw_update', {'pixels': args.pixels})

    def handle_query(self, query: str) -> Any:
        if query == "pixels":
            return self.pixels
