import sys
import asyncio
import websockets

USERS = set()


async def notify(ws, data):
    tasks = [user.send(data) for user in USERS if user != ws]
    if len(tasks):
        await asyncio.gather(*tasks)


async def danmaku(ws, path):
    try:
        USERS.add(ws)
        async for message in ws:
            await notify(ws, message)
    finally:
        USERS.remove(ws)


async def start(PORT):
    server = await websockets.serve(danmaku, '127.0.0.1', PORT)
    print("Websocket is running at PORT: %d" % PORT)
    await server.wait_closed()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You haven't set the port of websocket!")
        exit(1)
    asyncio.run(start(int(sys.argv[1])))
