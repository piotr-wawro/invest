from datetime import date
from enum import Enum
import json
from pathlib import Path


class Unit(Enum):
    OZ = 'oz'

class Currency(Enum):
    PLN = 'pln'

class Asset(Enum):
    GOLD = 'gold'

class Ratio:
    def __init__(self, data) -> None:
        self.name: str = data['name']
        self.ratio: int = data['ratio']

    def __repr__(self) -> str:
        return f'{{name: {self.name}, ratio: {self.ratio}}}'

class WalletRatio:
    def __init__(self, data) -> None:
        self.quick = [Ratio(x) for x in data['quick']]
        self.short = [Ratio(x) for x in data['short']]
        self.long = [Ratio(x) for x in data['long']]

    def __repr__(self) -> str:
        return f'{{quick: {self.quick}, short: {self.short}, long: {self.long}}}'

class Investment:
    def __init__(self, data) -> None:
        self.asset: Asset = Asset(data['name'])
        self.date: date = date.fromisoformat(data['date'])
        self.price: float = data['price']
        self.currency: Currency = Currency(data['currency'])
        self.quantity: float = data['quantity']
        self.unit: Unit = Unit(data['unit'])

    def __repr__(self) -> str:
        return f'{{name: {self.asset}, date: {self.date}, price: {self.price}, currency: {self.currency}, quantity: {self.quantity}, unit: {self.unit}}}'

class WalletInvestments:
    def __init__(self, data) -> None:
        self.quick = [Investment(x) for x in data['quick']]
        self.short = [Investment(x) for x in data['short']]
        self.long = [Investment(x) for x in data['long']]

    def __repr__(self) -> str:
        return f'{{quick: {self.quick}, short: {self.short}, long: {self.long}}}'

class Wallet:
    def __init__(self, path: str) -> None:
        with Path(path).open() as file:
            data = json.load(file)
        self.wallet_ratio = WalletRatio(data['wallet_ratio'])
        self.investments = WalletInvestments(data['investments'])

    def __repr__(self) -> str:
        return f'{{wallet_ratio: {self.wallet_ratio}, investments: {self.investments}}}'
