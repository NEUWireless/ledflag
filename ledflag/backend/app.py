from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO
from iotbridge.server import Server
from ledflag.bridge.message import Instruction
from ledflag.bridge.message import ModeQuery as Query
from ledflag.controller.modes.text import *
from ledflag.controller.modes.draw import *
import eventlet
import numpy as np

# Needed for iotbridge threading
eventlet.monkey_patch()

# Create message server for sending instructions to LED flag
ms = Server()
print("Connecting to the LED Matrix...")
ms.connect()

# Create flask application
app = Flask(__name__, static_folder="build/static", template_folder="build")
socketio = SocketIO(app, message_queue="redis://")


# Index route: serve React application
@app.route('/')
def index():
    return render_template("index.html")


# Display scrolling text
@app.route('/scrolltext')
def display_scrolling_text():
    text = request.args.get('text', default="NU Wireless")
    ms.task(Instruction(TextMode, TextArgs(text, 16)))
    return "ok"


# Handle draw commands
@socketio.on('draw')
def handle_draw(draw):
    pixels = draw['pixels']
    print(pixels)
    ms.task(Instruction(DrawMode, DrawArgs(pixels)))


# Retrieve state of LEDs (in draw mode)
@app.route('/draw/get')
def query_draw():
    pixels = ms.query(Query(DrawMode, "pixels"))
    if not pixels:
        return "LED Flag not in draw mode", 500
    return jsonify({'pixels': list(map(list, pixels))})


# Clear all LEDs (in draw mode)
@app.route('/clear')
def clear():
    ms.task(Instruction(DrawMode, DrawArgs([])))
    return "ok"


# Image upload
@app.route('/image', methods=['POST'])
def image():
    data = request.json.get('data')
    data_len = len(data)
    assert data_len == 64*32*4
    np_arr = np.array(data)
    np_arr.shape = (32, 64, 4)
    pixels = []
    for y in range(32):
        for x in range(64):
            pix = np_arr[y][x]
            pixels.append({'x': x, 'y': y, 'r': int(pix[0]), 'g': int(pix[1]), 'b': int(pix[2])})
    print(pixels[:3])
    ms.task(Instruction(DrawMode, DrawArgs(pixels)))
    return "ok"


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
