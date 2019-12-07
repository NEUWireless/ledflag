from ledflag.bridge.message import DisplayText
from rgbmatrix import RGBMatrix, graphics
from time import sleep


def display_text(msg: DisplayText, matrix: RGBMatrix, **kwargs):
    print("Displaying text: {}".format(msg.text))
    font = graphics.Font()
    font.LoadFont("/home/pi/LED-Flag/ledflag/ledflag/controller/fonts/7x13.bdf")
    blue = graphics.Color(20, 235, 255)
    matrix.Clear()
    graphics.DrawText(matrix, font, 2, 10, blue, msg.text)


def display_scrolling_text(msg: DisplayText, matrix: RGBMatrix, **kwargs):
    free = kwargs['free']
    matrix.Clear()
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("/home/pi/LED-Flag/ledflag/ledflag/controller/fonts/7x13.bdf")
    color = graphics.Color(76, 245, 141)
    pos = offscreen_canvas.width
    my_text = msg.text

    while free():
        offscreen_canvas.Clear()
        text_length = graphics.DrawText(offscreen_canvas, font, pos, 19, color, my_text)
        pos -= 1
        if pos + text_length < 0:
            pos = offscreen_canvas.width
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        sleep(0.05)
