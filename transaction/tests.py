from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from .models import Courier, Transaction
from .models.transaction import TransactionType


class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.courier = Courier.objects.create(name="Courier 1")

    def test__calculate_daily_amount(self):
        transaction1 = Transaction.objects.create(
            transaction_type=TransactionType.INCREASE.value,
            courier=self.courier,
            amount=200,
            date=date.today(),
        )
        calculated_amount = transaction1._calculate_daily_amount()
        self.assertEqual(calculated_amount, Decimal(200))
        transaction2 = Transaction.objects.create(
            transaction_type=TransactionType.DECREASE.value,
            courier=self.courier,
            amount=50,
            date=date.today(),
        )
        calculated_amount = transaction2._calculate_daily_amount()
        self.assertEqual(calculated_amount, Decimal(150))

        transaction2 = Transaction.objects.create(
            transaction_type=TransactionType.TRIP.value,
            courier=self.courier,
            amount=50,
            date=date.today(),
        )
        calculated_amount = transaction2._calculate_daily_amount()
        self.assertEqual(calculated_amount, Decimal(200))
