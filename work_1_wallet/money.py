from dataclasses import dataclass
from decimal import Decimal

from currency import Currency
from exceptions import NotComparisonException, NegativeValueException


@dataclass
class Money:
    value: Decimal
    currency: Currency

    def __add__(self, money):
        self.currency_validate(money)
        return Money(self.value + money.value, currency=self.currency)

    def __sub__(self, money):
        self.currency_validate(money)
        money = Money(self.value - money.value, currency=self.currency)
        if money.is_positive():
            return money
        raise NegativeValueException(money)

    def currency_validate(self, obj):
        if self.currency != obj.currency:
            raise NotComparisonException(f'{self.currency} != {obj.currency}')

    def is_positive(self):
        return self.value > 0


class Wallet:

    def __init__(self, *args: Money):
        self.__cash: dict = {}
        self.add(*args)

    def __getitem__(self, key: Currency):
        return self.__cash.get(key, Money(Decimal('0'), currency=key))

    def __setitem__(self, key: Currency, value: Money):
        if key != value.currency:
            raise NotComparisonException
        self.__cash[key] = value

    def __delitem__(self, key: Currency):
        if key in self.__cash:
            del self.__cash[key]

    def __len__(self):
        return len(self.__cash)

    def add(self, money: Money):
        if money.currency not in self.__cash:
            self[money.currency] = Money(Decimal('0'), money.currency)
        self[money.currency] = self[money.currency] + money
        return self

    def sub(self, money):
        new_money = self[money.currency] - money
        if not new_money.is_positive():
            raise NegativeValueException
        self[money.currency] = new_money
        return self

    def __str__(self):
        return f'{self.__cash}'
