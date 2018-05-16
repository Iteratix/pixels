import socketio
import eventlet
import eventlet.wsgi
from flask import Flask
#import SWHear
#import numpy

from pyenttec import DMXConnection
sio = socketio.Server()
app = Flask(__name__)

#ear = SWHear.SWHear(rate=44100,updatesPerSecond=20)
#ear.stream_start()

d = DMXConnection(u'/dev/ttyUSB0')

class DMXFrame(object):
    # def __init__(self, dmx, ear):
    def __init__(self, dmx):
        self.dmx = dmx

    def render(self):
        self.dmx.render()

    def blackout(self):
        self.dmx.blackout()

    #BOBBY PAR
    # 1 func, 2 255 (rgbw), 3 spd, 4 main, 5-8 rgbw
    def set_pixel_a(self, dmx_id, red, green, blue, white):
        white = min([red, green, blue])/3
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

    #SET BARS
    #1-3 RGB, 4-6, RGB, 7-9 RGB 10 master
    def set_pixel_bar_a(self,dmx_id, red, green, blue, amber):
        white = min([red, green, blue])/3
        amber = min([red - white, green - white])/2
        red = red - white - amber
        green = green - white - amber
        blue = blue - white
        self.dmx.dmx_frame[dmx_id] = red
        self.dmx.dmx_frame[dmx_id+1] = green
        self.dmx.dmx_frame[dmx_id+2] = blue
        self.dmx.dmx_frame[dmx_id+3] = amber
        self.dmx.dmx_frame[dmx_id+9] = 255

    def set_pixel_bar_b(self,dmx_id, red, green, blue, amber):
        white = min([red, green, blue])/3
        amber = min([red - white, green - white])/2
        red = red - white - amber
        green = green - white - amber
        blue = blue - white
        self.dmx.dmx_frame[dmx_id+4] = red
        self.dmx.dmx_frame[dmx_id+5] = green
        self.dmx.dmx_frame[dmx_id+6] = blue
        self.dmx.dmx_frame[dmx_id+7] = amber   
        self.dmx.dmx_frame[dmx_id+9] = 255

def send_pixel(data):
    # f = DMXFrame(dmx=d, ear=ear)
    f = DMXFrame(dmx=d)

    for num, rgb_tuple in enumerate(data):
        dmx_id = num * 10

        #print("setting pixel: {} {}".format(dmx_id, rgb_tuple))
        
        if num < 4:
            f.set_pixel_b(dmx_id,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2], 0)
        if num > 3 and num < 8:
            f.set_pixel_a(dmx_id,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2], 0)
        if num == 8:
            f.set_pixel_bar_a(199,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2],100)
            f.set_pixel_bar_b(199,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2],100)
        if num == 9:
            f.set_pixel_bar_a(249,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2],100)
            f.set_pixel_bar_b(249,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2],100)

        #f.set_pixel_b(dmx_id,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2], 0)
    # f.set_pixel_a(40,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2], 0)
    # f.set_pixel_a(50,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2], 0)
    # f.set_pixel_a(60,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2], 0)
    # f.set_pixel_a(70,rgb_tuple[0],rgb_tuple[1],rgb_tuple[2], 0)
    f.render()
    # port.dmx_frame[42] = 255 # strobe in combo with ch1
    # port.dmx_frame[43] = rgb_tuple[0]
    # port.dmx_frame[44] = rgb_tuple[1]
    # port.dmx_frame[45] = rgb_tuple[2]
    # port.dmx_frame[46] = 0 #rgb_tuple[2]
    #port.render()

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
