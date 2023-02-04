from rest_framework import serializers
from financial_report.models import WeeklyReport
from transaction.serializers import CourierSerializer


class WeeklyReportSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(read_only=True)

    class Meta:
        model = WeeklyReport
        fields = "__all__"
