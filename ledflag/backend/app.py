from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO
from iotbridge.server import Server
from iotbridge.message import Query
from ledflag.bridge.message import Instruction
from ledflag.controller.mode import *
import eventlet
eventlet.monkey_patch()

ms = Server()
print("Connecting to the LED Matrix...")
ms.connect()

app = Flask(__name__, static_folder="build/static", template_folder="build")
# socketio = SocketIO(app)
socketio = SocketIO(app, message_queue="redis://")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/scrolltext')
def display_scrolling_text():
    text = request.args.get('text', default="NU Wireless")
    ms.task(Instruction(TextMode, {'text': text, 'size:': 16}))
    return "ok"


@socketio.on('draw')
def handle_draw(draw):
    pixels = draw['pixels']
    print(pixels)
    ms.task(Instruction(DrawMode, {'pixels': pixels}))
    # socketio.emit('draw_update', {'pixels': pixels})


@app.route('/draw/get')
def query_draw():
    pixels = ms.query(Query("pixels"))
    if not pixels:
        return "Unable to process query", 500
    return jsonify({'pixels': list(map(list, pixels))})


@app.route('/clear')
def clear():
    ms.task(Instruction(DrawMode, {'pixels': []}))
    return "ok"


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
