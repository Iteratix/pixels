import socketio
import eventlet
import eventlet.wsgi
import random

from flask import Flask

import pyenttec as dmx
sio = socketio.Server(cors_allowed_origins="*")
app = Flask(__name__)

try:
    d = dmx.DMXConnection(u'/dev/ttyUSB0')
except:
    d = dmx.select_port()

class DMXFrame(object):
    def __init__(self, dmx):
        self.dmx = dmx
        #dmx.set_refresh_rate(0)

    def render(self):
        self.dmx.render()

    def blackout(self):
        self.dmx.blackout()

    def set_pixel_wecan(self, dmx_id, red, green, blue):
        dmx_id = dmx_id -1

        white = int(min([red, green, blue])*0.4)
        red = red - white
        green = green - white
        blue = blue - white
        self.dmx.dmx_frame[dmx_id] = 255 #shutter
        self.dmx.dmx_frame[dmx_id+1] = int(red/3) #red?
        self.dmx.dmx_frame[dmx_id+2] = int(green/3) #green
        self.dmx.dmx_frame[dmx_id+3] = int(blue/3) #blue
        self.dmx.dmx_frame[dmx_id+4] = int(white/3) # white
        self.dmx.dmx_frame[dmx_id+5] = 0 # strobe
        self.dmx.dmx_frame[dmx_id+6] = 0 # open ch1-5
        self.dmx.dmx_frame[dmx_id+7] = 0 # program 


    def set_pixel_shehds(self, dmx_id, red, green, blue):
        dmx_id = dmx_id -1

        white = int(min([red, green, blue])*0.4)
        red = red - white
        green = green - white
        blue = blue - white

        self.dmx.dmx_frame[dmx_id] = 255 #shutter
        self.dmx.dmx_frame[dmx_id+1] = int(red/3) #red?
        self.dmx.dmx_frame[dmx_id+2] = int(green/3) #green
        self.dmx.dmx_frame[dmx_id+3] = int(blue/3) #blue
        self.dmx.dmx_frame[dmx_id+4] = int(white/3) # white
        self.dmx.dmx_frame[dmx_id+5] = 0 # amber
        self.dmx.dmx_frame[dmx_id+6] = 255 # violet
        self.dmx.dmx_frame[dmx_id+7] = 0 # strobe 
        self.dmx.dmx_frame[dmx_id+8] = 0 # macro/sound control 
        self.dmx.dmx_frame[dmx_id+9] = 0 # macro speed


    #Betopper
    def set_pixel_washbar(self, dmx_id, red, green, blue):
        dmx_id = dmx_id -1

        white = int(min([red, green, blue])*0.4)
        red = red - white
        green = green - white
        blue = blue - white

        self.dmx.dmx_frame[dmx_id] = 255 #shutter
        self.dmx.dmx_frame[dmx_id+1] = red #red?
        self.dmx.dmx_frame[dmx_id+2] = green #green
        self.dmx.dmx_frame[dmx_id+3] =  blue #blue
        self.dmx.dmx_frame[dmx_id+4] = 0 # uv
        self.dmx.dmx_frame[dmx_id+5] = 0 # func
        self.dmx.dmx_frame[dmx_id+6] = 0 # func2
        self.dmx.dmx_frame[dmx_id+7] = 0 # speed


    #Betopper
    def set_pixel_betopper(self, dmx_id, red, green, blue):
        dmx_id = dmx_id -1

        white = int(min([red, green, blue])*0.4)
        red = red - white
        green = green - white
        blue = blue - white

        self.dmx.dmx_frame[dmx_id] = 255 #shutter
        self.dmx.dmx_frame[dmx_id+1] = 0 #strobe?
        self.dmx.dmx_frame[dmx_id+2] = 0 #green
        self.dmx.dmx_frame[dmx_id+3] =  0 #blue
        self.dmx.dmx_frame[dmx_id+4] = red # red
        self.dmx.dmx_frame[dmx_id+5] = green# green
        self.dmx.dmx_frame[dmx_id+6] = blue # blue
        self.dmx.dmx_frame[dmx_id+7] = 0 #


    #JLPOW
    def set_pixel_jlpow(self, dmx_id, red, green, blue):
        dmx_id = dmx_id - 1

        white = int(min([red, green, blue])*0.4)
        red = red - white
        green = green - white
        blue = blue - white

        self.dmx.dmx_frame[dmx_id+0] = 0
        self.dmx.dmx_frame[dmx_id+1] = 255
        self.dmx.dmx_frame[dmx_id+2] = 0
        self.dmx.dmx_frame[dmx_id+3] = 255
        self.dmx.dmx_frame[dmx_id+4] = red
        self.dmx.dmx_frame[dmx_id+5] = green
        self.dmx.dmx_frame[dmx_id+6] = blue


    #BOBBY PAR VERSION 2
    # 1 main dim, 2,3,4,5 rgbw, 6 strobe, 7 modes, 8 speed
    def set_pixel_aa(self, dmx_id, red, green, blue):
        #dmx offset for these
        dmx_id = dmx_id - 1

        white = int(min([red, green, blue])*0.4)
        red = red - white
        green = green - white
        blue = blue - white

        self.dmx.dmx_frame[dmx_id+0] = 255
        self.dmx.dmx_frame[dmx_id+1] = red
        self.dmx.dmx_frame[dmx_id+2] = green
        self.dmx.dmx_frame[dmx_id+3] = blue
        self.dmx.dmx_frame[dmx_id+4] = white
        self.dmx.dmx_frame[dmx_id+5] = 0
        self.dmx.dmx_frame[dmx_id+6] = 0
        self.dmx.dmx_frame[dmx_id+7] = 0
        self.dmx.dmx_frame[dmx_id+8] = 0

    #BOBBY PAR, 
    # 1 func, 2 255 (rgbw), 3 spd, 4 main, 5-8 rgbw
    def set_pixel_a(self, dmx_id, red, green, blue):
        white = int(min([red, green, blue])*0.4)
        red = red - white
        green = green - white
        blue = blue - white
        # for color in [white, amber, red, green, blue]:
        #     if color >= 255: color = color - (color - 255)
        self.dmx.dmx_frame[dmx_id+0] = 255
        self.dmx.dmx_frame[dmx_id+2] = 255
        self.dmx.dmx_frame[dmx_id+3] = red
        self.dmx.dmx_frame[dmx_id+4] = green
        self.dmx.dmx_frame[dmx_id+5] = blue
        self.dmx.dmx_frame[dmx_id+6] = white


    #CLAY PAR
    # :dimmer, :strobe, :control, :speed, :red, :green, :blue, :white
    def set_pixel_b(self, dmx_id, red, green, blue, white):
        if dmx_id != 0:
            dmx_id = dmx_id - 1
        white = min([red, green, blue])/4
        # amber = min([red - white, green - white])/2
        red = int((red - white) * 0.50)
        green = int((green - white) * 0.50)
        blue = int((blue - white) * 0.50)
        self.dmx.dmx_frame[dmx_id] = 255
        self.dmx.dmx_frame[dmx_id+1] = 0
        self.dmx.dmx_frame[dmx_id+2] = 0
        self.dmx.dmx_frame[dmx_id+3] = 0
        self.dmx.dmx_frame[dmx_id+4] = red
        self.dmx.dmx_frame[dmx_id+5] = green
        self.dmx.dmx_frame[dmx_id+6] = blue
        self.dmx.dmx_frame[dmx_id+7] = white


def send_pixel(data):
    f = DMXFrame(dmx=d)
    
    for num, rgb_tuple in enumerate(data):
        dmx_id = num * 10
        #print(num, rgb_tuple)
        
        if num > 0 and num < 10: #dmx ids 0-100
            #print("setting shehds: {} {}".format(dmx_id, rgb_tuple))
            f.set_pixel_shehds(dmx_id,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2])

        if num >= 10 and num < 14: #100-200 
            #print("setting jlpow: {} {}".format(dmx_id, rgb_tuple))
            f.set_pixel_betopper(dmx_id,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2])

        if num >= 15 and num < 16: #100-200 
            #print("setting wecan: {} {}".format(dmx_id, rgb_tuple))
            f.set_pixel_wecan(dmx_id,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2])

        # if num >= 30 and num < 40:
        #     print("setting typea: {} {}".format(dmx_id, rgb_tuple))
        #     f.set_pixel_a(dmx_id,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2])

        # if num >= 40 and num < 50:
        #     print("setting typeb: {} {}".format(dmx_id, rgb_tuple))
        #     f.set_pixel_aa(dmx_id,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2])

    f.render()


@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat message', namespace='/chat')
def message(sid, data):
    #print("message ", data)
    send_pixel(data)

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 9000)), app)
