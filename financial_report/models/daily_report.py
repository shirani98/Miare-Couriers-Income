from django.db import models
from transaction.models.courier import Courier
from datetime import date, timedelta
from django.db.models import Sum
from django.db import transaction


class DailyReport(models.Model):
    """
    Model representing a daily report of the courier's earnings.
    """    
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE,related_name='daily_reports',verbose_name="Courier")
    amount = models.PositiveIntegerField(
        default=0, verbose_name="Amount"
    )
    date = models.DateField(default=date.today,verbose_name="Date")

    def __str__(self):
        return f"{self.courier.name} | {self.amount} | {self.date}"

    class Meta:
        unique_together = ("courier", "date")
        ordering = ('-date',)
        
    def _calculate_amount(self,start_week):
        """Helper method to calculate the amount.

        The amount is calculated by summing all transactions with start and end time.
        """
        end_week = start_week + timedelta(days=7)
        return DailyReport.objects.filter(
            date__gte=start_week,
            date__lt=end_week,
            courier=self.courier,
        ).aggregate(total_weekly_income=Sum("amount"))["total_weekly_income"]

    def save(self, *args, **kwargs):
        from financial_report.models import WeeklyReport

        super().save(*args, **kwargs)
        start_week = self.date - timedelta(days=(self.date.weekday() + 2) % 7)
        with transaction.atomic():
            WeeklyReport.objects.update_or_create(
                courier=self.courier,
                date=start_week,
                defaults={"amount": self._calculate_amount(start_week)},
            )
