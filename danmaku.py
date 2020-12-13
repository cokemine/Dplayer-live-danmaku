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


async def start():
    server = await websockets.serve(danmaku, 'localhost', 8765)
    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(start())
