"""Classes for melon orders."""
from random import randrange
import datetime


class AbstractMelonOrder():
    """ Melon order from any country."""

    def __init__(self, species, qty):
        """Initialize melon order attributes."""

        self.species = species
        self.qty = qty
        if self.qty > 100:
            raise TooManyMelonsError("No more than 100 melons!")
        self.shipped = False

    def get_base_price(self, splurge=False):
        base_price = 5
        now = datetime.datetime.now()
        if splurge is True:
            base_price = randrange(5, 10)
        if (now.hour in range(8, 11)) and now.weekday() in range(0, 5):
            base_price += 4
        return base_price

    def get_total(self, splurge=False):
        """Calculate price, including tax."""

        base_price = self.get_base_price(splurge)

        if self.species == "Christmas melon":
            base_price *= 1.5

        total = (1 + self.tax) * self.qty * base_price

        # if (self.qty < 10) and (self.order_type == "international"):
        #     total += 3

        return total

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""
        self.shipped = True


class TooManyMelonsError(ValueError):
    """ Exception raised when too many melons are ordered. """


class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    order_type = "domestic"
    tax = 0.08


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""
    tax = 0.17
    order_type = "international"

    def __init__(self, species, qty, country_code):
        """Initialize melon order attributes."""
        super().__init__(species, qty)
        self.country_code = country_code

    def get_total(self):
        total = super().get_total()
        if self.qty < 10:
            return total + 3

        return total

    def get_country_code(self):
        """Return the country code."""

        return self.country_code


class GovernmentMelonOrder(AbstractMelonOrder):

    order_type = "government"
    tax = 0
    passed_inspection = False

    def mark_inspection(self, passed):
        self.passed_inspection = passed
