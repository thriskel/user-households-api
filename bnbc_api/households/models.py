from django.db import models
from users import models as users_models


class Household(models.Model):
    identifier = models.CharField(
        verbose_name="Identifier",
        max_length=150
    )
    user = models.ForeignKey(
        users_models.User,
        on_delete=models.RESTRICT
    )
    country = models.CharField(
        verbose_name="Country",
        max_length=50
    )
    city = models.CharField(
        verbose_name="City",
        max_length=50
    )
    road = models.CharField(
        verbose_name="Road",
        max_length=150
    )
