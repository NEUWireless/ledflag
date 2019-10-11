from typing import TypeVar
from PIL import Image

class DisplayText:

    def __init__(self, text: str, size: int):
        self.text = text
        self.size = size

    def __str__(self):
        return "DisplayText: {} @ size {}".format(self.text, self.size)


class DisplayImage:

    def __init__(self, image: Image):
        self.image = image

    def __str__(self):
        return "DisplayImage: {} x {} px".format(self.image.width, self.image.height)


Message = TypeVar('Message', DisplayText, DisplayImage)
