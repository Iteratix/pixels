from pyenttec import DMXConnection
from random import randint
from time import sleep

port = DMXConnection(u'/dev/tty.usbserial-6A2I3O5P')

# port.dmx_frame[0] = 11
while True:
    port.dmx_frame[3] = 255 # strobe in combo with ch1
    port.dmx_frame[4] = 255
    port.dmx_frame[5] = randint(0,255)
    port.dmx_frame[6] = randint(0,255)
    port.dmx_frame[7] = randint(0,255)
    port.render()
    sleep(0.1)

# for channel in range(3, 9):
#     port.dmx_frame[channel] = 255
#     port.render()
