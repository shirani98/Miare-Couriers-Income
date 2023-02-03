from django.db import models
from transaction.models.courier import Courier

class Transaction(models.Model):
    TRIP = 1
    INCREASE = 2
    DECREASE = 3

    TRANSACTION_TYPE_CHOICE = ((INCREASE, "Increase"), (DECREASE, "Decrease"), (TRIP, "Trip"))
    
    transaction_type = models.SmallIntegerField(choices=TRANSACTION_TYPE_CHOICE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    description = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.courier.name} - {self.amount} - {self.get_transaction_type_display()}"
