import asyncio
import os
import aiohttp.web
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))
async def testhandle(request):
    return aiohttp.web.Response(text='Test handle')
async def compra(ws):
    print("compra !!!!!")
    await asyncio.sleep(5)
    await ws.send_str("Su compra ya fue procesada :)" + '/answer server')
    print("finish !!!!")
async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')
    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(msg.data)
            if msg.data == 'close':
                await ws.close()
            elif msg.data == 'compra':
                fast_val = asyncio.create_task(compra(ws))  
            else:
                await ws.send_str(msg.data + '/answer server ')
    print('Websocket connection closed')
    return ws
def main():
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application()
    app.router.add_route('GET', '/', testhandle)
    app.router.add_route('GET', '/ws', websocket_handler)
    aiohttp.web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    main()