import pyenttec as dmx
from random import randint
from time import sleep
import launchpad_py as launchpad
from pygame import time

port = dmx.select_port()


red = 255
green = 0
blue = 0

white = int(min([red, green, blue])*0.4)

red = red - white
green = green - white
blue = blue - white

dmx_id = 9

# pad = launchpad.Launchpad()
# pad.Open()
# pad.ButtonFlush()

# # LedAllOn() test
# print( " - Testing LedAllOn()" )
# for i in [ 5, 21, 79, 3]:
#     pad.LedAllOn( i )
#     time.wait(500)
# pad.LedAllOn( 0 )

# # Testing RANDINT
while True:

    port.dmx_frame[dmx_id] = randint(0,255)
    port.dmx_frame[dmx_id+1] = randint(0,255)
    port.dmx_frame[dmx_id+2] = randint(0,255)
    port.dmx_frame[dmx_id+3] =  randint(0,255)
    port.dmx_frame[dmx_id+4] = randint(0,255)
    port.dmx_frame[dmx_id+5] = randint(0,255)
    port.dmx_frame[dmx_id+6] = randint(0,255)
    port.dmx_frame[dmx_id+7] = randint(0,255)


    port.render()
    sleep(0.1)

red = 0

# # Wash Light Bar
# while True:
#     events = pad.ButtonStateRaw()

#     if events != []:
#         if events[1] > 0:
#             print(events)
#             key = events[0]

#             if(key == 112):
#                 red = red + 10


#     port.dmx_frame[dmx_id] = 255 #shutter
#     port.dmx_frame[dmx_id+1] = red #red
#     port.dmx_frame[dmx_id+2] = 0 #green
#     port.dmx_frame[dmx_id+3] =  0 #blue
#     port.dmx_frame[dmx_id+4] = 0 # uv
#     port.dmx_frame[dmx_id+5] = 0# function
#     port.dmx_frame[dmx_id+6] = 0 # function 2
#     port.dmx_frame[dmx_id+7] = 0 # speed


#     port.render()
#     sleep(0.1)

# # Wash Light Bar
# while True:
    
#     port.dmx_frame[dmx_id] = 255 #shutter
#     port.dmx_frame[dmx_id+1] = red #red
#     port.dmx_frame[dmx_id+2] = 0 #green
#     port.dmx_frame[dmx_id+3] =  0 #blue
#     port.dmx_frame[dmx_id+4] = 0 # uv
#     port.dmx_frame[dmx_id+5] = 0# function
#     port.dmx_frame[dmx_id+6] = 0 # function 2
#     port.dmx_frame[dmx_id+7] = 0 # speed


#     port.render()
#     sleep(0.1)

# # Betopper LC200W-H
while True:

    port.dmx_frame[dmx_id] = 255 #shutter
    port.dmx_frame[dmx_id+1] = 0 #strobe?
    port.dmx_frame[dmx_id+2] = 0 #green
    port.dmx_frame[dmx_id+3] =  0 #blue
    port.dmx_frame[dmx_id+4] = 255 # red
    port.dmx_frame[dmx_id+5] = 0# green
    port.dmx_frame[dmx_id+6] = 0 # blue
    port.dmx_frame[dmx_id+7] = 0 #

    print(dmx_id, red, green, blue, white)
    port.render()
    sleep(0.1)

# # Chauvet Swarm 5
# DMX -1
# while True:

#     port.dmx_frame[dmx_id] = 255 #func
#     port.dmx_frame[dmx_id+1] = 10 #LED colors
#     port.dmx_frame[dmx_id+2] = 0 #LED speed
#     port.dmx_frame[dmx_id+3] = 0 #LED strobe
#     port.dmx_frame[dmx_id+4] = 110 #White LED
#     port.dmx_frame[dmx_id+5] = 25 #Laser
#     port.dmx_frame[dmx_id+6] = 1 #Laser Strobe
#     port.dmx_frame[dmx_id+7] = 200 #LED motor
#     port.dmx_frame[dmx_id+8] = 0 #Laser Motor


#     port.render()
#     sleep(0.1)


# # JLPOW
# DMX - 1
# while True:

#     port.dmx_frame[dmx_id] = 0 #func
#     port.dmx_frame[dmx_id+1] = 255 #color mode
#     port.dmx_frame[dmx_id+2] = 0 #speed
#     port.dmx_frame[dmx_id+3] = 255 # master
#     port.dmx_frame[dmx_id+4] = 255 #red
#     port.dmx_frame[dmx_id+5] = 255 #green #MASTER DIMMER?
#     port.dmx_frame[dmx_id+6] = 255 #blue

#     port.render()
#     sleep(0.1)


# PAR TYPE B
# while True:
#     port.dmx_frame[dmx_id+0] = 255
#     port.dmx_frame[dmx_id+1] = red
#     port.dmx_frame[dmx_id+2] = green
#     port.dmx_frame[dmx_id+3] = blue
#     port.dmx_frame[dmx_id+4] = white
#     port.dmx_frame[dmx_id+5] = 0
#     port.dmx_frame[dmx_id+6] = 0
#     port.dmx_frame[dmx_id+7] = 0
#     port.dmx_frame[dmx_id+8] = 0
#     port.render()
#     sleep(0.1)


# while True:
#     port.dmx_frame[dmx_id+0] = 255
#     port.dmx_frame[dmx_id+2] = 255
#     port.dmx_frame[dmx_id+3] = red
#     port.dmx_frame[dmx_id+4] = green
#     port.dmx_frame[dmx_id+5] = blue
#     port.dmx_frame[dmx_id+6] = white

#     print(dmx_id, red, green, blue, white)

#     port.render()
#     sleep(0.1)

# while True:
#     port.dmx_frame[10] = 255 # strobe in combo with ch1
#     port.dmx_frame[11] = 255
#     port.dmx_frame[12] = randint(0,255)
#     port.dmx_frame[13] = randint(0,255)
#     port.dmx_frame[14] = randint(0,255)
#     port.render()
#     sleep(0.1)

# for channel in range(3, 9):
#     port.dmx_frame[channel] = 255
#     port.render()
