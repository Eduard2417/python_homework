from abc import abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Order:
    price: Decimal


class Discount():

    @abstractmethod
    def apply(self, price: Decimal) -> Decimal:
        pass


class PercentDiscount(Discount):

    def __init__(self, percent: Decimal):
        self.percent = percent

    def apply(self, price: Decimal) -> Decimal:
        discount_amount = (self.percent / Decimal('100')) * price
        return price - discount_amount


class FixDiscount(Discount):

    def __init__(self, discount_amount: Decimal):
        self.discount_amount = discount_amount

    def apply(self, price: Decimal) -> Decimal:
        return price - self.discount_amount


class LoyaltyDiscount(Discount):

    def __init__(self, loyalty_level: int):
        self.loyalty_level = loyalty_level

    def apply(self, price: Decimal) -> Decimal:
        loyalty_discount = Decimal(self.loyalty_level * 10)
        return price - loyalty_discount


class DiscountGetter():

    @abstractmethod
    def get_discount_classes(self):
        pass


class DefaultDiscountGetter(DiscountGetter):

    def get_discount_classes(self, percent_count, fix_count):
        return [(PercentDiscount, Decimal(percent_count)),
                (FixDiscount, Decimal(fix_count))]


class DiscountApplier:

    def __init__(self, order, discount_types):
        self.order = order
        self.discount_types = discount_types

    def apply_discounts(self):
        final_price = self.order.price
        for discount_type, arg in self.discount_types:
            discount = discount_type(arg)
            final_price = discount.apply(final_price)
        return final_price
