from flask import Flask, request, render_template
from ledflag.bridge.server import MessageServer
from ledflag.bridge.message import DisplayText, DisplayScrollingText


ms = MessageServer()
print("Waiting for matrix connection...")
ms.connect()

app = Flask(__name__, static_folder="build/static", template_folder="build")


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
