import socketio
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print("connect", sid)

@sio.event
async def message(sid, data):
    await sio.emit("message", data)

@sio.event
async def disconnect(sid):
    print("disconnect", sid)
