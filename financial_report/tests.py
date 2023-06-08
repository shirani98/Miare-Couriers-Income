from datetime import date, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from financial_report.models import WeeklyReport
from financial_report.serializers import WeeklyReportSerializer
from financial_report.tasks import DailyReport, WeeklyReport, generate_weekly_report
from transaction.models import Courier, Transaction


class GenerateWeeklyReportTestCase(TestCase):
    @patch("financial_report.tasks.date")
    def test_generate_weekly_report(self, mock_date):
        first_courier = Courier.objects.create(name="Courier_one")
        second_courier = Courier.objects.create(name="Courier_two")

        # Set the current date to a Saturday
        mock_date.today.return_value = date(2023, 1, 7)

        # Create sample DailyReport instances for first_courier
        DailyReport.objects.create(courier_id=first_courier.id, date=date(2022, 12, 29), amount=100)
        DailyReport.objects.create(courier_id=first_courier.id, date=date(2023, 1, 1), amount=100)
        DailyReport.objects.create(courier_id=first_courier.id, date=date(2023, 1, 2), amount=200)
        DailyReport.objects.create(courier_id=first_courier.id, date=date(2023, 1, 3), amount=300)
        DailyReport.objects.create(courier_id=first_courier.id, date=date(2023, 1, 7), amount=400)
        DailyReport.objects.create(courier_id=first_courier.id, date=date(2023, 1, 8), amount=900)

        # Create sample DailyReport instances for second_courier
        DailyReport.objects.create(courier_id=second_courier.id, date=date(2022, 12, 29), amount=100)
        DailyReport.objects.create(courier_id=second_courier.id, date=date(2023, 1, 2), amount=200)
        DailyReport.objects.create(courier_id=second_courier.id, date=date(2023, 1, 3), amount=150)
        DailyReport.objects.create(courier_id=second_courier.id, date=date(2023, 1, 4), amount=200)
        DailyReport.objects.create(courier_id=second_courier.id, date=date(2023, 1, 7), amount=500)
        DailyReport.objects.create(courier_id=second_courier.id, date=date(2023, 1, 8), amount=900)

        weekly_reports = WeeklyReport.objects.all()
        self.assertEqual(weekly_reports.count(), 0)

        generate_weekly_report()

        weekly_reports = WeeklyReport.objects.filter(date=date(2023, 1, 7))
        self.assertEqual(weekly_reports.count(), 2)

        self.assertTrue(weekly_reports.filter(courier_id=first_courier.id, amount=1000).exists())
        self.assertTrue(weekly_reports.filter(courier_id=second_courier.id, amount=1050).exists())


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
            date=date.today() + timedelta(days=2),
            amount=300,
        )
        generate_weekly_report()

    def test_get_all_weekly_reports(self):
        response = self.client.get(reverse("weekly-reports-list"))

        weekly_reports = WeeklyReport.objects.all()
        serialized = WeeklyReportSerializer(weekly_reports, many=True)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_zero_weekly_reports_by_date_range(self):
        response = self.client.get(
            reverse("weekly-reports-list"),
            {
                "from_date": date.today() + timedelta(days=15),
                "to_date": date.today() + timedelta(days=25),
            },
        )

        weekly_reports = WeeklyReport.objects.filter(
            date__gte=date.today() + timedelta(days=15),
            date__lte=date.today() + timedelta(days=25),
        )
        serialized = WeeklyReportSerializer(weekly_reports, many=True)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_two_weekly_reports_by_date_range(self):
        response = self.client.get(
            reverse("weekly-reports-list"),
            {
                "from_date": date.today(),
                "to_date": date.today() + timedelta(days=10),
            },
        )

        weekly_reports = WeeklyReport.objects.filter(
            date__gte=date.today() ,
            date__lte=date.today() + timedelta(days=10),
        )
        serialized = WeeklyReportSerializer(weekly_reports, many=True)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
