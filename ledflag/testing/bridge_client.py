from ledflag.bridge.client import MessageClient
from time import sleep

mc = MessageClient()
mc.listen(lambda m: print(m))

sleep(10)
