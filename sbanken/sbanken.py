from typing import List

from .auth import Auth
from .account import Account
from .const import BANK_SCOPE


class SbankenAPI:
    """ Class for communication with Sbanken API """

    def __init__(self, auth: Auth):
        """ Initialize API and store Auth """
        self.auth = auth

    async def async_get_accounts(self) -> List[Account]:
        response = await self.auth.request("get", f"{BANK_SCOPE}/accounts/")
        response.raise_for_status()
        # print(await response.json())

        j = await response.json()

        return [Account(account_data, self.auth) for account_data in j["items"]]

    # def get_accounts(self) -> List[Account]:
    #    """ Return all accounts """
    #    response = self.auth.request("get", f"{BANK_SCOPE}/accounts/")
    #    response.raise_for_status()
    #    return [Account(account_data, self.auth) for account_data in response.json()]

    async def async_get_account(self, accountId: str) -> Account:
        """ Return the account data """
        response = await self.auth.request("get", f"{BANK_SCOPE}/accounts/{accountId}")
        response.raise_for_status()
        return Account(await response.json(), self.auth)
