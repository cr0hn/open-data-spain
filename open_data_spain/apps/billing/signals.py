from django.dispatch import receiver
from django.db.models.signals import post_init

from .models import Plan
from .sdk.plans import PlanFeatures


@receiver(post_init, sender=Plan)
def load_plan(sender, instance, **kwargs):
    if instance.features:
        instance._plan_features = PlanFeatures(**instance.features)

