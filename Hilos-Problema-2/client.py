import asyncio
import logging
from aiohttp import ClientSession, ClientWebSocketResponse
from aiohttp.http_websocket import WSMessage
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('client')
async def subscribe_to_messages(websocket: ClientWebSocketResponse) -> None:
    async for message in websocket:
        if isinstance(message, WSMessage):
            logger.info('> Message from server received: %s', message)
async def make_purchase(websocket: ClientWebSocketResponse) -> None:
    while True:
        message = "compra"
        logger.info('< Sending message: %s', message)
        await websocket.send_str(message)
        await asyncio.sleep(2)
async def echo_handler() -> None:
    async with ClientSession() as session:
        async with session.ws_connect('ws://127.0.0.1:8080/ws', ) as ws:
            send_message_task = asyncio.create_task(make_purchase(websocket=ws))
            subscribe_to_messages_task = asyncio.create_task(subscribe_to_messages(websocket=ws))
            done, pending = await asyncio.wait(
                [send_message_task, subscribe_to_messages_task], return_when=asyncio.FIRST_COMPLETED,
            )
            if not ws.closed:
                await ws.close()
            for task in pending:
                task.cancel()
if __name__ == '__main__':
    asyncio.run(echo_handler())