from rest_framework import generics, response
from .models import Expense
from .serializers import ExpenseSerializer
from django.contrib.auth import get_user_model
from django.db import models


class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = []


class ExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = []


class ExpenseDateRangeView(generics.ListAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        username = self.request.GET.get("username")

        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        expense_filter = {}

        if username:
            expense_filter["user"] = get_user_model().objects.get(username=username)

        if start_date and end_date:
            expense_filter["date__range"] = [start_date, end_date]
        if start_date and not end_date:
            expense_filter["date__gte"] = start_date
        if not start_date and end_date:
            expense_filter["date__lte"] = end_date

        return Expense.objects.filter(**expense_filter)


class ExpenseCategorySummaryView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        username = self.request.GET.get("username")
        year = self.request.GET.get("year")
        month = self.request.GET.get("month")

        expense_filter = {}

        if username:
            expense_filter["user"] = get_user_model().objects.get(username=username)
        if year:
            expense_filter["date__year"] = year
        if month:
            expense_filter["date__month"] = month

        summary = (
            Expense.objects.filter(**expense_filter)
            .values("category")
            .annotate(total=models.Sum("amount"))
        )
        return response.Response(summary)
