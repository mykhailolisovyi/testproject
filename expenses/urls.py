from django.urls import path
from .views import (
    ExpenseListCreateView,
    ExpenseRetrieveUpdateDestroyView,
    ExpenseDateRangeView,
    ExpenseCategorySummaryView,
)

urlpatterns = [
    path("", ExpenseListCreateView.as_view(), name="expense-list-create"),
    path("date-range/", ExpenseDateRangeView.as_view(), name="expense-date-range"),
    path(
        "category-summary/",
        ExpenseCategorySummaryView.as_view(),
        name="expense-category-summary",
    ),
    path("<int:pk>/", ExpenseRetrieveUpdateDestroyView.as_view(), name="expense-detail"),
]
