from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from financial_report.models import WeeklyReport
from financial_report.serializers import WeeklyReportSerializer
from transaction.models.transaction import Transaction
from transaction.models import Courier
from datetime import date, timedelta


class WeeklyReportListViewTestCase(APITestCase):
    def setUp(self):
        Courier_sample = Courier.objects.create(name="Courier")
        Transaction.objects.create(
            transaction_type=1, courier=Courier_sample, date=date.today(), amount=100
        )
        Transaction.objects.create(
            transaction_type=1,
            courier=Courier_sample,
            date=date.today() + timedelta(days=1),
            amount=200,
        )
        Transaction.objects.create(
            transaction_type=1,
            courier=Courier_sample,
            date=date.today() + timedelta(days=10),
            amount=300,
        )

    def test_get_all_weekly_reports(self):
        # hit the API endpoint
        response = self.client.get(reverse("weekly-reports-list"))

        # fetch the data from db
        weekly_reports = WeeklyReport.objects.all()
        serialized = WeeklyReportSerializer(weekly_reports, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_zero_weekly_reports_by_date_range(self):
        # hit the API endpoint
        response = self.client.get(
            reverse("weekly-reports-list"),
            {
                "from_date": date.today() + timedelta(days=15),
                "to_date": date.today() + timedelta(days=25),
            },
        )

        # fetch the data from db
        weekly_reports = WeeklyReport.objects.filter(
            date__gte=date.today() + timedelta(days=15),
            date__lte=date.today() + timedelta(days=25),
        )
        serialized = WeeklyReportSerializer(weekly_reports, many=True)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_two_weekly_reports_by_date_range(self):
        # hit the API endpoint
        response = self.client.get(
            reverse("weekly-reports-list"),
            {
                "from_date": date.today(),
                "to_date": date.today() + timedelta(days=10),
            },
        )

        # fetch the data from db
        weekly_reports = WeeklyReport.objects.filter(
            date__gte=date.today() ,
            date__lte=date.today() + timedelta(days=10),
        )
        serialized = WeeklyReportSerializer(weekly_reports, many=True)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
