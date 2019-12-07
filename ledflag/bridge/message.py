from typing import TypeVar


class DisplayText:

    def __init__(self, text: str, size: int):
        self.text = text
        self.size = size

    def __str__(self):
        return "DisplayText: {} @ size {}".format(self.text, self.size)


class DisplayScrollingText:

    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return "DisplayScrollingText: {}".format(self.text)


class DisplayImage:

    def __init__(self, image_file: str):
        self.image_file = image_file

    def __str__(self):
        return "DisplayImage: {}".format(self.image_file)


class Draw:

    def __init__(self, pixels):
        self.pixels = pixels

    def __str__(self):
        return "Draw {} Pixels".format(len(self.pixels))


class Clear:

    def __str__(self):
        return "Clear"


Message = TypeVar('Message', DisplayText, DisplayScrollingText, DisplayImage, Draw, Clear)
