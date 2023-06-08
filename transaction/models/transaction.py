from datetime import date
from enum import Enum

from django.apps import apps
from django.db import models, transaction
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce

from transaction.models import Courier


class TransactionType(Enum):
    """Enum class to represent the type of a Transaction."""

    TRIP = 1
    INCREASE = 2
    DECREASE = 3


class Transaction(models.Model):
    """
    Model to represent a Transaction.

    A transaction represents a financial transaction between the company and a courier.
    """

    transaction_type = models.SmallIntegerField(
        choices=[(type.value, type.name) for type in TransactionType],
        verbose_name="Transaction Type",
    )
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE,related_name='transactions')
    amount = models.PositiveIntegerField(
        default=0, verbose_name="Amount"
    )
    date = models.DateField(default=date.today, verbose_name="Date")
    description = models.JSONField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return f"{self.courier.name} - {self.amount} - {TransactionType(self.transaction_type).name}"

    def _calculate_daily_amount(self):
        """Helper method to calculate the amount.

        The amount is calculated by summing all positive transactions (TRIP and INCREASE) and
        subtracting all negative transactions (DECREASE).
        """
        total_amount = Coalesce(
            Sum(
                "amount",
                filter=Q(
                    transaction_type__in=[
                        TransactionType.TRIP.value,
                        TransactionType.INCREASE.value,
                    ]
                ),
            ),
            0,
        ) - Coalesce(Sum("amount", filter=Q(transaction_type=TransactionType.DECREASE.value)), 0)


        return self.courier.transactions.filter(date=self.date).aggregate(
            total_amount=total_amount
        )["total_amount"]

    def save(self, *args, **kwargs):
        DailyReport = apps.get_model(app_label="financial_report", model_name="DailyReport")

        super().save(*args, **kwargs)
        with transaction.atomic():
            DailyReport.objects.update_or_create(
                courier=self.courier,
                date=self.date,
                defaults={"amount": self._calculate_daily_amount()},
            )
