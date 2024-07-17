# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from . import models as user_models
from . import serializers as user_serializers
from households import serializers as households_serializers
from households import models as households_models

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.db.models import RestrictedError, Q


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """

    queryset = user_models.User.objects.all().order_by("id")
    serializer_class = user_serializers.UserSerializer
    # permission_classes = [TokenHasReadWriteScope]

    def get_serializer_class(self, *args, **kwargs):
        extra_action_creational_methods = ["POST", "PUT", "PATCH"]
        extra_actions = ["households", "edit_household"]
        if (
            self.action in extra_actions
            and self.request.method in extra_action_creational_methods
        ):
            return households_serializers.HouseholdSerializer
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RestrictedError:
            raise ValidationError(
                f"Can't delete the user {
                    instance.username}, because it has related households"
            )
        except Exception as e:
            raise ValidationError(str(e))

    @action(detail=True, methods=["GET", "DELETE", "POST"])
    def households(self, request, pk=None):
        user = self.get_object()

        households = households_models.Household.objects.filter(user=user)

        if request.method == "GET":
            country_filter = request.query_params.get("country")
            city_filter = request.query_params.get("city")
            road_filter = request.query_params.get("road")
            filters = Q()

            if country_filter:
                filters |= Q(country__icontains=country_filter)
            if city_filter:
                filters |= Q(city__icontains=city_filter)
            if road_filter:
                filters |= Q(road__icontains=road_filter)

            if filters:
                households = households.filter(filters)

            household_serializer = households_serializers.HouseholdSerializer(
                households, many=True
            )

            return Response(household_serializer.data)

        elif request.method == "DELETE":
            households.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        elif request.method == "POST":
            serializer = households_serializers.HouseholdSerializer(
                data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["PUT", "PATCH", "DELETE"],
        url_path=r"households/(?P<household_pk>\d+)",
    )
    def edit_household(self, request, pk=None, household_pk=None):
        household = households_models.Household.objects.get(id=household_pk)

        if request.method == "PUT":
            serializer = households_serializers.HouseholdSerializer(
                household, data=request.data
            )
        elif request.method == "PATCH":
            serializer = households_serializers.HouseholdSerializer(
                household, data=request.data, partial=True
            )
        elif request.method == "DELETE":
            try:
                household.delete()
            except Exception as e:
                raise ValidationError(str(e))
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
