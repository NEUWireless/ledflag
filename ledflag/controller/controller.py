from ledflag.bridge.client import MessageClient
from ledflag.bridge.message import Message, DisplayText, DisplayImage
from datetime import datetime


def message_handler(msg: Message):
    """
    Handles each incoming message from the message server, calling the appropriate
    function for each message to update the LED matrix.

    :param msg: The message from the server
    :return: None
    """

    # Print a debug statement
    print("[{}] Received > {}".format(
        datetime.now().strftime("%I:%M%p"), msg)
    )

    # Determine the type of the message (DisplayText, DisplayImage, etc.)
    msg_type = type(msg)

    if msg_type == DisplayText:
        print("Displaying text...")
        # Call display text function here

    elif msg_type == DisplayImage:
        print("Displaying image...")
        # Call display image function here


# Start the message client
mc = MessageClient()
mc.listen(message_handler)
