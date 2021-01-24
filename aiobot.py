import json
import sys
import asyncio
import pandas as pd
import numpy as np

from AsyncOanda.Pricing import Pricing

async def display(queue):
    while True:
        await asyncio.sleep(0.25) # Need tuning
        if queue:
            print(queue.pop(0))
            print(len(queue))

def get_removable(tick, ticks, rate):
    dummy_ticks = ticks.append(tick)
    ohlc = dummy_ticks.resample(rate).ohlc()

    #len(candle_stick) - size
    return len(ohlc) - 1

async def stack_ticks(rate, queue):
    ticks = pd.Series([])
    ohlcs = []
    while True:
        await asyncio.sleep(0.25) # Need tuning
        if queue:
            tick = queue.pop(0)

            price = float(tick["bids"][0]["price"])
            time = pd.to_datetime(tick["time"])
            tick = pd.Series(price, index=[time])
            print(f"{time} : {price}")

            removable_ohlc = get_removable(tick, ticks, rate)
            if removable_ohlc > 0:
                ohlc = ticks.resample(rate).ohlc()
                # concat_ohlc -> ohlcs
                # drop_ohlc
                ticks = pd.Series([])
                print(rate, ohlc)

            ticks = ticks.append(tick)

async def broadcast(src, dsts):
    while True:
        await asyncio.sleep(0.25) # 0.25だと少なくともキューづまりがない

        tmp = []
        for ele in src:
            tmp.append(src.pop(0))

        for dst in dsts:
            dst[:] = tmp[:]

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        credentials = json.load(f)
        id_ = credentials["oanda_id"]
        token = credentials["oanda_token"]

    instruments = "GBP_JPY"

    time_frames = {
        # "rate": queue
        "1min": [], 
        "5min": [], 
    }

    pricing = Pricing(id_=id_, token=token)
    loop = asyncio.get_event_loop()

    asyncio.ensure_future(pricing.stream(instruments))
    asyncio.ensure_future(broadcast(pricing.queue, list(time_frames.values())))

    for rate, queue in time_frames.items():
        asyncio.ensure_future(stack_ticks(rate, queue))

    loop.run_forever()
