import socketio
import eventlet
import eventlet.wsgi
from flask import Flask

from pyenttec import DMXConnection

port = DMXConnection('/dev/ttyUSB0')

sio = socketio.Server()
app = Flask(__name__)

def send_pixels(rgb_tuples):
    # print("sending pixel: {}".format(rgb_tuples))
    port.dmx_frame[33] = 255
    for rgb_tuple in rgb_tuples:
        rgb_tuple.append(0)
    # port.dmx_frame[33] = randint(0,255)
    for channel, value in enumerate(sum(rgb_tuples, [])):
        # for channel in range(0, 31):
        port.dmx_frame[channel] = value
    # sleep(0.1)
    port.render()

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat message', namespace='/chat')
def message(sid, data):
    # print("message ", data)
    send_pixels(data)

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 9000)), app)
