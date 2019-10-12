from ledflag.bridge.message import DisplayText
from rgbmatrix import RGBMatrix, graphics


def display_text(msg: DisplayText, matrix: RGBMatrix):
    font = graphics.LoadFont("fonts/7x13.bdf")
    blue = graphics.Color(20, 235, 255)
    graphics.DrawText(matrix, font, 2, 10, blue, msg.text)
