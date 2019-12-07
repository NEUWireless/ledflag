from ledflag.bridge.message import Draw, Clear
from rgbmatrix import RGBMatrix, graphics


def draw_pixels(msg: Draw, matrix: RGBMatrix, **kwargs):
    offset_canvas = matrix.CreateFrameCanvas()
    for pixel in msg.pixels:
        offset_canvas.SetPixel(pixel['x'], pixel['y'], pixel['r'], pixel['g'], pixel['b'])
    matrix.SwapOnVSync(offset_canvas)


def clear(msg: Clear, matrix: RGBMatrix, **kwargs):
    matrix.Fill(0, 0, 0)
