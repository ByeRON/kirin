from dataclasses import InitVar, dataclass, field


@dataclass
class Endpoints:
    _id: str
    _token: InitVar[str]
    _demo: bool = True
    _api_url: str = field(init=False)
    _stream_url: str = field(init=False)
    _headers: dict = field(default_factory=dict)

    def __post_init__(self, _token):
        env = "fxpractice.oanda.com"
        if self._demo is False:
            env = "fxtrade.oanda.com"

        self._api_url = f"https://api-{env}/v3"
        self._stream_url = f"https://stream-{env}/v3"
        self._headers = {"Authorization": f"Bearer {_token}"}
