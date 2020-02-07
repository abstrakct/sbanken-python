import json

from typing import Optional, Union, Callable, Dict

from requests import Response
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError, BackendApplicationClient
from abc import ABC, abstractmethod
from aiohttp import ClientSession, ClientResponse

from .const import API_ROOT, AUTH_ROOT


class Auth:
    """ Abstract class to make authenticated requests """

    def __init__(
        self,
        websession: ClientSession,
        customer_id: str = None,
        client_id: str = None,
        client_secret: str = None,
    ):
        self.websession = websession
        self.customer_id = customer_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    async def async_get_access_token(self) -> str:
        """ Return a valid access token """
        if self.token is None:
            oauth2_client = BackendApplicationClient(client_id=self.client_id)
            self.session = OAuth2Session(client=oauth2_client)
            self.token = self.session.fetch_token(
                token_url=f"{AUTH_ROOT}/identityserver/connect/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
            )
            self.websession.access_token = self.token

        return self.token["access_token"]

        # print(token)

        # async with self.websession.get(
        #    f"{AUTH_ROOT}/identityserver/connect/token",
        #    json={"client_id": self.client_id, "secret": self.client_secret},
        # ) as r:
        #    print(r.status)

    async def request(self, method, url, **kwargs) -> ClientResponse:
        """ Make a request """
        headers = kwargs.get("headers")

        if headers is None:
            headers = {"customerId": self.customer_id}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"

        return await self.websession.request(
            method, f"{API_ROOT}/{url}", **kwargs, headers=headers
        )


# class Auth:
#    def __init__(
#        self,
#        token: Optional[Dict[str, str]] = None,
#        customer_id: str = None,
#        client_id: str = None,
#        client_secret: str = None,
#        token_updater: Optional[Callable[[str], None]] = None,
#    ):
#
#        self.auth_host = AUTH_ROOT
#        self.api_host = API_ROOT
#        self.customer_id = customer_id
#        self.client_id = client_id
#        self.client_secret = client_secret
#        self.token_updater = token_updater
#
#        extra = {"client_id": self.client_id, "secret": self.client_secret}
#
#        oauth2_client = BackendApplicationClient(client_id=client_id)
#        self._oauth = OAuth2Session(
#            client=oauth2_client,
#            auto_refresh_kwargs=extra,
#            client_id=client_id,
#            token=token,
#            token_updater=token_updater,
#        )
#
#    def refresh_tokens(self) -> Dict[str, Union[str, int]]:
#        """ Refresh and return new tokens """
#        token = self._oauth.fetch_token(
#            token_url=f"{self.auth_host}/identityserver/connect/token",
#            client_id=self.client_id,
#            client_secret=self.client_secret,
#        )
#
#        if self.token_updater is not None:
#            self.token_updater(token)
#
#        return token
#
#    def request(self, method: str, path: str, **kwargs) -> Response:
#        """ Make a request """
#        url = f"{self.api_host}/{path}"
#        try:
#            return getattr(self._oauth, method)(
#                url, headers={"customerId": self.customer_id}, **kwargs
#            )
#        except TokenExpiredError:
#            self._oauth.token = self.refresh_tokens()
#            return getattr(self._oauth, method)(
#                url, headers={"customerId": self.customer_id}, **kwargs
#            )
#
#
