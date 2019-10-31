from flask import Flask, request
from ledflag.bridge.server import MessageServer
from ledflag.bridge.message import DisplayText, DisplayScrollingText


ms = MessageServer()
print("Waiting for matrix connection...")
ms.connect()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'LED Flag @ NU Wireless'


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
