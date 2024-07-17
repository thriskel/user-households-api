from rest_framework import serializers
from . import models as household_models


class HouseholdSerializer(serializers.ModelSerializer):

    class Meta:
        model = household_models.Household
        fields = ['id', 'identifier', 'country', 'city', 'road', 'user']
