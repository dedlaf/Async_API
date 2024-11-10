import asyncio
import websockets

uri = "ws://chat:8085"


async def spammer():
    nickname = 'dedlaf'
    async with websockets.connect(uri) as websocket:
        await websocket.send(nickname)
        await websocket.send('?')

        wait_peoples = True
        while wait_peoples:
            peoples = await websocket.recv()
            peoples = peoples.split(', ')
            if nickname in peoples:
                wait_peoples = False

        peoples.remove(nickname)
        while True:
            for name in peoples:
                for _ in range(10):
                    await websocket.send(f'{name}: Привет, мир! Это спаааааам!"')
            await asyncio.sleep(1)


loop = asyncio.get_event_loop()
loop.run_until_complete(spammer())
