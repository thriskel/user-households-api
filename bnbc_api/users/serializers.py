from .models import User
from households import models as household_models
from households import serializers as household_serializers
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    households = serializers.SerializerMethodField()

    def get_households(self, obj):
        households = household_models.Household.objects.filter(user=obj)
        household_serializer = household_serializers.HouseholdSerializer(
            households, many=True
        )

        return household_serializer.data

    class Meta:
        model = User
        fields = ["url", "username", "email", "households"]
