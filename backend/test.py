#!/usr/bin/env python
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw
from time import sleep

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 2
options.parallel = 0
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options=options)
image = Image.new("RGB", (matrix.height, matrix.width))
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, 63, 31), fill=(0, 0, 0), outline=(0, 0, 255))
draw.line((0, 0, 63, 31), fill=(200, 150, 20))
draw.line((0, 63, 31, 0), fill=(0, 25, 140))

matrix.Clear()
matrix.SetImage(image)

sleep(10)
matrix.Clear()
