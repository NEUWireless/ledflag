from ledflag.bridge.server import MessageServer
from ledflag.bridge.message import DisplayText

ms = MessageServer()
ms.connect()

text = DisplayText("Hello World", 16)
ms.send(text)

ms.close()
