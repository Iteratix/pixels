import socketio
import eventlet
import eventlet.wsgi
from flask import Flask

from pyenttec import DMXConnection

port = DMXConnection('/dev/ttyUSB0')

sio = socketio.Server()
app = Flask(__name__)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def send_pixels(rgb_tuples):
    # print("sending pixel: {}".format(rgb_tuples))
    for bar_number, bar_rgb_tuples in enumerate(chunks(rgb_tuples, 8)):
        if bar_number == 0:
            offset = 0
        else:
            offset = bar_number * 34
        brightness_channel = 33 + offset
        # print('brightness_channel: {}'.format(brightness_channel))
        port.dmx_frame[brightness_channel] = 255
        for rgb_tuple in bar_rgb_tuples:
            rgb_tuple.append(0)
            #print(rgb_tuple)
        for channel, value in enumerate(sum(bar_rgb_tuples, [])):
            # print("channel: {} value: {}".format(channel+offset, value))
            port.dmx_frame[channel+offset] = value
        # port.dmx_frame[33] = randint(0,255)
        # for channel, value in enumerate(sum(rgb_tuples, [])):
            # for channel in range(0, 31):
            # port.dmx_frame[channel] = value
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
