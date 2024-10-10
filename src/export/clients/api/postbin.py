import requests
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
        self.bin_data = self._create_bin()

    def _create_bin(self):
        resp = requests.post(f"{self.BASE_URL}/api/bin")
        resp.raise_for_status()
        return resp.json()

    def post_data(self, http_client, *args, **kwargs) -> str:
        """
        returns req_id
        """
        if time.time() > self.bin_data["expires"]:
            self.bin_data = self._create_bin()

        kwargs["url"] = f"{self.BASE_URL}/{self.bin_data["binId"]}"
        resp: requests.Response = http_client.request(*args, **kwargs)
        resp.raise_for_status()

        req_id = resp.text.strip()

        req_url = f"{self.BASE_URL}/api/bin/{self.bin_data['binId']}/req/{req_id}"
        logger.debug(f"Request url: {req_url}")

        return req_id
