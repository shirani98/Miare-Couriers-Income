
from rest_framework import generics
from financial_report.models import WeeklyReport
from financial_report.serializers import WeeklyReportSerializer
from django.db.models import Q
from typing import List


class WeeklyReportListView(generics.ListAPIView):
    """
    A view to list all the Weekly Reports in the system.
    """

    queryset = WeeklyReport.objects.all()
    serializer_class = WeeklyReportSerializer

    def get_queryset(self) -> List[WeeklyReport]:
        """
        Override get_queryset method to filter Weekly Reports based on from_date and to_date parameters
        in the request query parameters.

        Returns:
            List of Weekly Reports filtered by the given date range.
        """
        from_date = self.request.query_params.get("from_date")
        to_date = self.request.query_params.get("to_date")

        if from_date and to_date:
            queryset = WeeklyReport.objects.filter(
                Q(date__gte=from_date) & Q(date__lte=to_date)
            )
        else:
            queryset = WeeklyReport.objects.all()

        return queryset
