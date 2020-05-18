import asyncio
import websockets
import json
import zlib
from pt.libs.utils import set_logging
import logging
from optparse import OptionParser

async def handle_combos():
    while 1:
        logging.info("handle_combos...")
        await asyncio.sleep(1)


def pako_inflate_raw(data):
    decompress = zlib.decompressobj(-15)
    decompressed_data = decompress.decompress(data)
    decompressed_data += decompress.flush()
    return decompressed_data


async def handle_websockets_msg(websocket):
    while True:
        recv_text = await websocket.recv()
        data_raw = pako_inflate_raw(recv_text)
        data = json.loads(data_raw)
        if "errorCode" in data.keys() and data['errorCode'] > 0:
            logging.error(data['message'])
        else:
            if "data" in data.keys():
                logging.info(data)

async def main_logic(paire):
    url = "wss://okexcomreal.bafang.com:8443/ws/v3"
    async with websockets.connect('wss://okexcomreal.bafang.com:8443/ws/v3') as websocket:
        logging.info(url)
        await websocket.send(json.dumps(dict(
            op="subscribe",
            args=["spot/ticker:"+paire],
        )))
        await handle_websockets_msg(websocket)


if __name__ == '__main__':
    parser = OptionParser()
    set_logging(logging.INFO)
    parser.add_option("-c", "--combo", dest="combo",
                      help="货币组合: BTC-USDT")

    (options, args) = parser.parse_args()
    combo = options.combo if options.combo is not None else "BTC-USDT"

    loop = asyncio.get_event_loop()
    tasks = []
    task = asyncio.ensure_future(main_logic(combo))
    tasks.append(task)
    tasks.append(asyncio.ensure_future(handle_combos()))
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
