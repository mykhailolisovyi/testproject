from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Expense
from datetime import date

User = get_user_model()


class ExpenseTests(APITestCase):
    def setUp(self):
        # Set up test users and expenses
        self.user1 = User.objects.create_user(username="user1", email="user1@email.com")
        self.user2 = User.objects.create_user(username="user2", email="user2@email.com")

        self.expense1 = Expense.objects.create(
            user=self.user1, category="Food", amount=50, date=date(2024, 11, 1)
        )
        self.expense2 = Expense.objects.create(
            user=self.user1, category="Travel", amount=100, date=date(2024, 11, 2)
        )
        self.expense3 = Expense.objects.create(
            user=self.user2, category="Entertainment", amount=75, date=date(2024, 11, 3)
        )
        self.expense4 = Expense.objects.create(
            user=self.user2, category="Other", amount=125, date=date(2024, 10, 3)
        )

    def test_list_expenses(self):
        url = reverse("expense-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Expense.objects.count())

    def test_create_expense(self):
        url = reverse("expense-list-create")
        data = {
            "user": self.user1.username,
            "title": "Some title",
            "category": "Utilities",
            "amount": 150.5,
            "date": "2024-11-04",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 5)

    def test_retrieve_expense(self):
        url = reverse("expense-detail", args=[self.expense1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.expense1.id)

    def test_update_expense(self):
        url = reverse("expense-detail", args=[self.expense1.id])
        data = {"category": "Other"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense1.refresh_from_db()
        self.assertEqual(self.expense1.category, "Other")

    def test_delete_expense(self):
        url = reverse("expense-detail", args=[self.expense1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=self.expense1.id).exists())

    def test_filter_by_username(self):
        url = reverse("expense-date-range")
        response = self.client.get(url, {"username": "user1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only user1"s expenses

    def test_filter_by_date_range(self):
        url = reverse("expense-date-range")
        response = self.client.get(url, {"start_date": "2024-11-01", "end_date": "2024-11-02"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_category_summary(self):
        url = reverse("expense-category-summary")
        response = self.client.get(url, {"username": "user1", "year": "2024", "month": "11"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        summary_data = {item["category"]: item["total"] for item in response.data}
        self.assertEqual(
            summary_data,
            {
                "Food": 50,
                "Travel": 100,
            },
        )

    def test_category_summary_by_month(self):
        url = reverse("expense-category-summary")
        response = self.client.get(url, {"year": "2024", "month": "10"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        summary_data = {item["category"]: item["total"] for item in response.data}
        self.assertEqual(
            summary_data,
            {
                "Other": 125,
            },
        )
