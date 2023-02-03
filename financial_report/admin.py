from django.contrib import admin
from financial_report.models import DailyReport
from financial_report.models import WeeklyReport

admin.site.register(DailyReport)
admin.site.register(WeeklyReport)
