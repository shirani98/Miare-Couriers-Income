from django.db import models
from transaction.models.courier import Courier


class WeeklyReport(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.courier.name} - {self.amount}"

