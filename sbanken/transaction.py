from .auth import Auth
from .const import BANK_SCOPE


class Transaction:
    """ Class that represents a transaction in Sbanken """

    def __init__(self, raw_data: dict, auth: Auth):
        if "item" in raw_data:
            self.raw_data = raw_data["item"]
        else:
            self.raw_data = raw_data
        self.auth = auth

    @property
    def accounting_date(self) -> str:
        return self.raw_data["accountingDate"]
