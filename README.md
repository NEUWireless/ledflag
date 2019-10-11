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
