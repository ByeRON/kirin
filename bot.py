import json
import sys
import time

from retry import retry

from SyncOanda.Pricing import Pricing

@retry(delay=1, backoff=2, max_delay=60)
def connect_to_stream(endpoint, instruments):
    print("start or restart connecting to stream")

    response = pricing.stream(instruments)
    response.raise_for_status()
    for line in response.iter_lines():
        if line:
            recv = json.loads(line.decode("UTF-8"))
            print(recv)

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        credentials = json.load(f)
        id_ = credentials["oanda_id"]
        token = credentials["oanda_token"]

    instruments = "GBP_JPY"

    pricing = Pricing(id_=id_, token=token)
    connect_to_stream(pricing, instruments)
