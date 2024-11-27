from rest_framework import serializers
from .models import Expense
from django.contrib.auth import get_user_model


class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(),
        slug_field="username",
    )

    class Meta:
        model = Expense
        fields = ["id", "user", "title", "amount", "date", "category"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be positive.")
        return value
