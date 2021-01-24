from aiohttp import ClientSession
import asyncio
import json

from CommonOanda.Endpoints import Endpoints


class Pricing(Endpoints):
    def __init__(self, id_: str, token: str, demo: bool = True):
        super().__init__(_id=id_, _token=token, _demo=demo)
        self.queue = []

    async def get(self, instruments):
        url = f"{self._api_url}/accounts/{self._id}/pricing"
        params = {"instruments": instruments}
        async with ClientSession() as session:
            async with session.get(url, headers=self._headers, params=params) as response:
                print(await response.content.readline())

    async def stream(self, instruments):
        url = f"{self._stream_url}/accounts/{self._id}/pricing/stream"
        params = {"instruments": instruments}

        while True:
            try:
                async with ClientSession() as session:
                    async with session.get(url, headers=self._headers, params=params) as response:
                        async for line in response.content:
                            msg = str(line, encoding="utf-8").rstrip("\n")
                            recv = json.loads(msg)

                            if recv["type"] == "HEARTBEAT":
                                continue

                            self.queue.append(recv)

            except asyncio.TimeoutError as e:
               print(e) 
               continue
