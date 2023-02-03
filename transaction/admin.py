from django.contrib import admin
from transaction.models import Courier
from transaction.models import Transaction


admin.site.register(Courier)
admin.site.register(Transaction)