import orjson

from django.db import models
from django.contrib.auth import get_user_model

from model_utils.models import TimeStampedModel, UUIDModel

from .sdk.plans import PlanNames, get_plan_features, PlanFeatures


class MonthlyRequestsPerUser(TimeStampedModel, models.Model):
    id = models.IntegerField(primary_key=True)
    requests = models.IntegerField(default=0)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='monthly_requests')

    class Meta:
        verbose_name = 'Monthly requests per user'
        verbose_name_plural = 'Monthly requests per user'


class Plan(TimeStampedModel, UUIDModel, models.Model):
    """
    Los planes son los que definen unas características concretas para los usuarios.
    """
    name = models.CharField(max_length=100, choices=PlanNames.PLAN_NAMES, default=PlanNames.FREE)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='billing_plan')
    features = models.JSONField(default=dict, blank=True, null=True)

    active = models.BooleanField(default=True)

    expiration_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'

    def save(self, *args, **kwargs):
        # Only save features if plan is not enterprise. Enterprise plan are custom plans
        if self.name != PlanNames.ENTERPRISE:
            self.features = get_plan_features(self.name)

        super().save(*args, **kwargs)

    @property
    def plan_features(self) -> PlanFeatures | None:
        return self._plan_features
