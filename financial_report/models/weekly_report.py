from django.db import models
from transaction.models.courier import Courier
from datetime import date

class WeeklyReport(models.Model):
    """
    Model representing a weekly report of the courier's earnings.
    """
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE,related_name='weekly_reports')
    amount = models.PositiveIntegerField(
        default=0, verbose_name="Amount"
    )
    date = models.DateField(default=date.today,verbose_name="Date")

    def __str__(self):
        return f"{self.courier.name} | {self.amount} | {self.date}"

    class Meta:
        unique_together = ("courier", "date")
        ordering = ('-date',)