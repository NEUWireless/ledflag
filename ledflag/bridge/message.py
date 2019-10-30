from typing import TypeVar


class DisplayText:

    def __init__(self, text: str, size: int):
        self.text = text
        self.size = size

    def __str__(self):
        return "DisplayText: {} @ size {}".format(self.text, self.size)


class DisplayImage:

    def __init__(self, image_file: str):
        self.image_file = image_file

    def __str__(self):
        return "DisplayImage: {}".format(self.image_file)


Message = TypeVar('Message', DisplayText, DisplayImage)
