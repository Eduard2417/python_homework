from dataclasses import dataclass
import enum
from typing import Literal


class AllowedCurrency(enum.Enum):
    RUB = enum.auto()
    USD = enum.auto()


@dataclass(slots=True, frozen=True, eq=True, repr=True)
class Currency:
    code: AllowedCurrency


@dataclass(slots=True, frozen=True, eq=True, repr=True)
class RUB(Currency):
    code: Literal[AllowedCurrency.RUB] = AllowedCurrency.RUB


@dataclass(slots=True, frozen=True, eq=True, repr=True)
class USD(Currency):
    code: Literal[AllowedCurrency.USD] = AllowedCurrency.USD


rub = RUB()
usd = USD()
