import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError

peoples = {}


async def welcome(websocket: websockets.WebSocketServerProtocol) -> str:
    await websocket.send('Добрый день! Напишите имя: \n')
    name = await websocket.recv()
    await websocket.send('Чтобы поговорить, напишите "<имя>: <сообщение>". Например: Иван: купи хлеб.')
    await websocket.send('Посмотреть список участников можно командой "?"')
    peoples[name.strip()] = websocket
    return name


async def receiver(websocket: websockets.WebSocketServerProtocol) -> None:
    name = await welcome(websocket)
    try:
        while True:
            message = (await websocket.recv()).strip()
            if message == '?':
                await websocket.send(', '.join(peoples.keys()))
                continue
            else:
                try:
                    to, text = message.split(': ', 1)
                    if to in peoples:
                        await peoples[to].send(f'Сообщение от {name}: {text}')
                    else:
                        await websocket.send(f'Пользователь {to} не найден')
                except ValueError:
                    await websocket.send(f'Не правильный формат сообщения! Попробуйте "<имя>: <сообщение>"')
    except ConnectionClosedError:
        del peoples[name.strip()]


async def main():
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

    ws_server = await websockets.serve(receiver, "0.0.0.0", 8085)

    await ws_server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
