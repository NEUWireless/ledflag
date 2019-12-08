from flask import Flask, request, render_template
from flask_socketio import SocketIO
from ledflag.bridge.server import MessageServer
from ledflag.bridge.message import *


ms = MessageServer()
print("Waiting for matrix connection...")
ms.connect()

app = Flask(__name__, static_folder="build/static", template_folder="build")
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/displaytext')
def display_text():
    text = request.args.get('text', default="NU Wireless")
    ms.send(DisplayText(text, 16))
    return "ok"


@app.route('/scrolltext')
def display_scrolling_text():
    text = request.args.get('text', default="NU Wireless")
    ms.send(DisplayScrollingText(text))
    return "ok"


@socketio.on('draw')
def handle_draw(draw):
    pixels = draw['pixels']
    print(pixels)
    ms.send(Draw(pixels))


@app.route('/clear')
def clear():
    ms.send(Clear())
    return "ok"


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
