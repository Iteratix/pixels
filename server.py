from aiohttp import web
import socketio


from pyenttec import DMXConnection

port = DMXConnection('/dev/ttyUSB0')

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

async def send_pixel(rgb_tuple):
    print("sending pixel: {}".format(rgb_tuple))
    port.dmx_frame[3] = 255 # strobe in combo with ch1
    port.dmx_frame[4] = 0
    port.dmx_frame[5] = rgb_tuple[0]
    port.dmx_frame[6] = rgb_tuple[1]
    port.dmx_frame[7] = rgb_tuple[2]
    port.render()

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat message', namespace='/chat')
async def message(sid, data):
    print("message ", data)
    # await sio.emit('reply', room=sid)
    await send_pixel(data[0])

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

app.router.add_static(
    '/',
    './',
    show_index=True
)
# app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, port=8000)
