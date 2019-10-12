from ledflag.bridge.message import DisplayText
from rgbmatrix import RGBMatrix, graphics
from PIL import Image


def display_text(msg: DisplayText, matrix: RGBMatrix):
    print("Displaying text: {}".format(msg.text))
    font = graphics.Font()
    font.LoadFont("fonts/7x13.bdf")
    blue = graphics.Color(20, 235, 255)
    matrix.Clear()
    graphics.DrawText(matrix, font, 2, 10, blue, msg.text)

"""
def display_text(msg: DisplayText, matrix: RGBMatrix):
    image = Image.open("banana.jpeg")
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    matrix.SetImage(image.convert('RGB'))
"""
