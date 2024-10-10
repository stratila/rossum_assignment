from aiohttp import ClientSession
import time
import logging
import sys

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


class ApiClient:
    BASE_URL = "https://www.postb.in"

    def __init__(self):
        self.bin_data = {"expires": 0}

    def set_client_session(self, client_session: ClientSession):
        self.client_session = client_session

    async def _create_bin(self):
        async with self.client_session.post(f"{self.BASE_URL}/api/bin") as resp:
            resp.raise_for_status()
            return await resp.json()

    async def post_data(self, *args, **kwargs) -> str:
        """
        returns req_id
        """
        if time.time() > self.bin_data["expires"]:
            self.bin_data = await self._create_bin()

        kwargs["url"] = f"{self.BASE_URL}/{self.bin_data["binId"]}"

        async with self.client_session.request(*args, **kwargs) as resp:
            resp.raise_for_status()
            req_id = await resp.text()

        req_url = f"{self.BASE_URL}/api/bin/{self.bin_data['binId']}/req/{req_id}"

        return req_url
