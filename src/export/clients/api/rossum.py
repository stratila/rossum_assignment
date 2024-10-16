import time
from aiohttp import ClientSession


class ApiClient:
    API_BASE = "https://{custom_domain}.rossum.app"
    API_VER = "api/v1"
    AUTH_ENDPOINT = "auth/login"
    ANNOTATIONS_ENDPOINT = "annotations"
    QUEUES_EXPORT_ENDPOINT = "queues/{queue_id}/export"

    def __init__(
        self,
        username: str,
        password: str,
        custom_domain: str,
    ):

        self.username = username
        self.password = password
        self.custom_domain = custom_domain
        self.api_base = self.API_BASE.format(custom_domain=self.custom_domain)
        self.token = None
        self.exp_time = None
        self.client_session = None

    def set_client_session(self, client_session: ClientSession):
        self.client_session = client_session

    async def __get_auth_token(self) -> str:
        if self.exp_time is None or (
            self.exp_time is not None and time.time() > self.exp_time
        ):
            async with self.client_session.post(
                url=f"{self.api_base}/{self.API_VER}/{self.AUTH_ENDPOINT}",
                json={
                    "username": self.username,
                    "password": self.password,
                },
            ) as resp:
                resp.raise_for_status()

                json = await resp.json()
                self.token = json.get("key", None)

                if self.token is None:
                    raise Exception("Token is empty")
                self.exp_time = time.time() + (162 * 3600)
        return self.token

    async def get_annotations(self) -> dict:
        auth_token = await self.__get_auth_token()
        async with self.client_session.post(
            url=f"{self.api_base}/{self.API_VER}/{self.ANNOTATIONS_ENDPOINT}",
            headers={"Authorization": f"Bearer {auth_token}"},
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def queue_export(
        self,
        queue_id: int,
        annotation_id: int,
        format: str = "xml",
    ) -> bytes:
        auth_token = await self.__get_auth_token()

        async with self.client_session.get(
            url=(
                f"{self.api_base}/{self.API_VER}/"
                f"{self.QUEUES_EXPORT_ENDPOINT.format(queue_id=queue_id)}"
            ),
            params={"format": format, "id": str(annotation_id)},
            headers={"Authorization": f"Bearer {auth_token}"},
        ) as resp:
            return await resp.read()
