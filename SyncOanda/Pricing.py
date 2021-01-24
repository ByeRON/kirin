import requests

from CommonOanda.Endpoints import Endpoints


class Pricing(Endpoints):
    def __init__(self, id_: str, token: str, demo: bool = True):
        super().__init__(_id=id_, _token=token, _demo=demo)

    def stream(self, instruments):
        url = f"{self._stream_url}/accounts/{self._id}/pricing/stream"
        params = {"instruments": instruments}
        return requests.get(url=url, headers=self._headers, params=params, stream=True)
