import asyncio

import httpx


class AVClient:
    def __init__(
        self,
        auth_client: httpx.AsyncClient,
        scan_client: httpx.AsyncClient,
        client_id: str,
        client_secret: str,
        auth_url: str,
        scan_url: str,
    ):
        self.auth_client = auth_client
        self.scan_client = scan_client

        self.client_id = client_id
        self.client_secret = client_secret

        self.auth_url = auth_url
        self.scan_url = scan_url

        self._token: str | None = None
        self._token_lock = asyncio.Lock()

    async def get_access_token(self) -> str:
        if self._token:
            return self._token

        async with self._token_lock:
            if self._token:
                return self._token

            response = await self.auth_client.post(
                self.auth_url,
                headers={
                    "Content-Type": "application/json",
                },
                json={
                    "userName": self.client_id,
                    "password": self.client_secret,
                },
            )
            response.raise_for_status()

            token = response.json().get("access_token")

            if not token:
                raise RuntimeError(
                    "AV response does not contain access_token"
                )

            self._token = token
            return token

    async def scan(
        self,
        filename: str,
        file_bytes: bytes,
        transaction_id: str,
    ):
        token = await self.get_access_token()

        response = await self._scan(
            token,
            filename,
            file_bytes,
            transaction_id,
        )

        # Refresh once if the AV token expired.
        if response.status_code == 401:
            async with self._token_lock:
                self._token = None

            token = await self.get_access_token()

            response = await self._scan(
                token,
                filename,
                file_bytes,
                transaction_id,
            )

        response.raise_for_status()

        return response.json(), response.headers

    async def _scan(
        self,
        token: str,
        filename: str,
        file_bytes: bytes,
        transaction_id: str,
    ) -> httpx.Response:
        return await self.scan_client.post(
            self.scan_url,
            headers={
                "Authorization": f"Bearer {token}",
                "x-tps-value-id": transaction_id,
            },
            files={
                "file": (
                    filename,
                    file_bytes,
                )
            },
        )

    async def close(self):
        await self.auth_client.aclose()
        await self.scan_client.aclose()
