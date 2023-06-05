from datetime import date, timedelta

from django.db import models
from django.db.models import Sum

from transaction.models.courier import Courier


class DailyReport(models.Model):
    """
    Model representing a daily report of the courier's earnings.
    """

    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, related_name="daily_reports", verbose_name="Courier")
    amount = models.BigIntegerField(default=0, verbose_name="Amount")
    date = models.DateField(default=date.today, verbose_name="Date")

    def __str__(self):
        return f"{self.courier.name} | {self.amount} | {self.date}"

    class Meta:
        unique_together = ("courier", "date")
        ordering = ('-date',)
