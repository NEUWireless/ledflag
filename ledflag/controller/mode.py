from rgbmatrix import RGBMatrix, graphics
from time import sleep
from iotbridge.message import Message
from flask_socketio import SocketIO
from typing import Dict


class Mode:

    def __init__(self, matrix: RGBMatrix, socketio: SocketIO):
        self.matrix = matrix
        self.socketio = socketio

    def run(self, args: Dict, **kwargs):
        pass


class DrawMode(Mode):

    def __init__(self, matrix: RGBMatrix, socketio: SocketIO):
        super().__init__(matrix, socketio)
        self.pixels = [(0, 0, 0)] * (matrix.width * matrix.height)
        self.matrix.Fill(0, 0, 0)
        self.canvas = self.matrix.CreateFrameCanvas()

    def run(self, args: Dict, **kwargs):
        if len(args['pixels']) == 0:
            self.canvas.Fill(0, 0, 0)
        else:
            for pixel in args['pixels']:
                self.pixels[pixel['y'] * self.matrix.width + pixel['x']] = (pixel['r'], pixel['g'], pixel['b'])
                self.canvas.SetPixel(pixel['x'], pixel['y'], pixel['r'], pixel['g'], pixel['b'])
            self.socketio.emit('draw_update', {'pixels': args['pixels']})
        self.canvas = self.matrix.SwapOnVSync(self.canvas)


class TextMode(Mode):

    def __init__(self, matrix: RGBMatrix, socketio: SocketIO):
        super().__init__(matrix, socketio)

    def run(self, args: Dict, **kwargs):
        free = kwargs['free']
        self.matrix.Clear()
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/home/pi/LED-Flag/ledflag/ledflag/controller/fonts/7x13.bdf")
        color = graphics.Color(76, 245, 141)
        pos = offscreen_canvas.width
        my_text = args['text']

        while free():
            offscreen_canvas.Clear()
            text_length = graphics.DrawText(offscreen_canvas, font, pos, 19, color, my_text)
            pos -= 1
            if pos + text_length < 0:
                pos = offscreen_canvas.width
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            sleep(0.05)
