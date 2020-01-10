# ledflag
LED Flag Project @ NU Wireless

**ledflag** is an ongoing project at the NU Wireless club.
The objective is to control a 32x64 matrix of addressable LEDs wirelessly through a web application,
with a variety of features planned. Displaying text, images, and the ability to draw only the matrix
are all intended functionalities of ledflag.

## Project Overview
The project currently consists of the following four sections:

### Backend
Flask server to handle web requests that tell the RGB matrix what to display.

### Controller
Handles drawing images on the RGB matrix.

### Bridge
Connects the Flask server to the RGB Matrix controller.

### Frontend
Web Application UI for user control of the RGB Matrix

## Testing
LED Matrix code can be tested conveniently using a Jupyter notebook. With the ledflag service stopped, navigate to the `ledflag` folder and run the following command to start the Jupyter notebook server:
```bash
$ sudo jupyter notebook --allow-root
```
Use the link it outputs to test your code in the browser. See the example provided in `ledflag/testing/Example.ipynb`.
Currently, led matrix functions take the following form:
```python
def display_scrolling_text(msg: DisplayText, matrix: RGBMatrix, **kwargs):
    ....
    free = kwargs['free']
    offscreen_canvas = matrix.CreateFrameCanvas()
    ...
    while free():
        text_length = graphics.DrawText(offscreen_canvas, font, pos, 19, color, msg.text)
        sleep(0.05)
    ...
```
`msg` is a Message that contains all the information necessary to display the content. In this example, it contains the text to be displayed on the LED Flag. `matrix` is the RGB Matrix object provided by the [rgbmatrix](https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python) library. It can be used to manipulate the pixels on the LED board. Lastly the keyword arguments provided by `**kwargs` contain the `free()` function, which should be used in place of an infinite loop to allow your code to exit when a new instruction is received. It returns false when a new instruction is waiting for your function to complete.

Each function requires a corresponding message to trigger it, which is placed in the `ledflag/bridge/message.py` file. The message for DisplayText is shown below:

```python
class DisplayText:

    def __init__(self, text: str, size: int):
        self.text = text
        self.size = size

    def __str__(self):
        return "DisplayText: {} @ size {}".format(self.text, self.size)
```
When the controller receives a DisplayText message, it will run the display_text function to display the given text.

If you're satisfied with your function, you can add it to the controller by modifying the `controller.py` file in `ledflag/controller`:

```python
from ledflag.bridge.message import *
from ledflag.controller.text import display_text, display_scrolling_text

msg_functions = {
    DisplayText: display_text,
    DisplayScrollingText: display_scrolling_text,
    Draw: draw_pixels,
    Clear: clear
}
```

First, import your function into the controller. Then modify the `msg_functions` dictionary to map the message you created to your function. This tells the controller to run your function when it receives the corresponding message.

If you would like to run the project in development mode, run these commands from two different shells:
```bash
ledflag/backend $ python3 app.py
```
```bash
ledflag/controller $ python3 controller.py
```
The first command runs the web server, while the second runs the LED controller.

## Production
To start the project in production mode, start the following services:
```bash
$ sudo systemctl start gunicorn.serivce
$ sudo systemctl start ledflag.service
$ sudo service nginx start
```
Since these services start on boot, you may need to stop them in order to test your own code.
