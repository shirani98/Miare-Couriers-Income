from datetime import date, timedelta

from celery import shared_task
from django.db import transaction
from django.db.models import OuterRef, Subquery, Sum

from financial_report.models import DailyReport, WeeklyReport


@shared_task
def generate_weekly_report():
    today = date.today()
    start_date = today - timedelta(days=6)
    end_date = today

    daily_reports = DailyReport.objects.filter(date__range=(start_date, end_date))

    subquery = (
        daily_reports.filter(courier=OuterRef("courier"))
        .values("courier")
        .annotate(total_amount=Sum("amount"))
        .values("total_amount")
    )

    weekly_report_data = (
        daily_reports.values("courier")
        .annotate(total_amount=Subquery(subquery))
        .values("courier", "total_amount")
        .distinct()
    )

    weekly_reports = [
        WeeklyReport(courier_id=data["courier"], date=end_date, amount=data["total_amount"])
        for data in weekly_report_data
    ]
    with transaction.atomic():
        WeeklyReport.objects.bulk_create(weekly_reports, ignore_conflicts=True)
