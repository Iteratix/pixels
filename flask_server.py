import socketio
import eventlet
import eventlet.wsgi
from flask import Flask

from pyenttec import DMXConnection

port = DMXConnection('/dev/ttyUSB0')

sio = socketio.Server()
app = Flask(__name__)

def send_pixel(rgb_tuple):
    print("sending pixel: {}".format(rgb_tuple))
    port.dmx_frame[3] = 255 # strobe in combo with ch1
    port.dmx_frame[4] = rgb_tuple[0]
    port.dmx_frame[5] = rgb_tuple[1]
    port.dmx_frame[6] = rgb_tuple[2]
    port.dmx_frame[7] = 0 #rgb_tuple[2]
    port.render()

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat message', namespace='/chat')
def message(sid, data):
    print("message ", data)
    send_pixel(data[0])

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 9000)), app)
