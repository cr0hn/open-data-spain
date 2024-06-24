from django import template

from apps.billing.sdk.plans import get_plan_features, PlanNames

register = template.Library()


@register.simple_tag
def free_plan(*args, **kwargs) -> dict:
    return get_plan_features(PlanNames.FREE)


@register.simple_tag(name="professional_plan")
def professional_plan() -> dict:
    return get_plan_features(PlanNames.PROFESSIONAL)


@register.simple_tag(name="premium_plan")
def premium_plan() -> dict:
    return get_plan_features(PlanNames.PREMIUM)


@register.simple_tag(name="enterprise_plan")
def enterprise_plan() -> dict:
    return get_plan_features(PlanNames.ENTERPRISE)


@register.simple_tag(name="pay_as_you_go_plan")
def pay_as_you_go_plan() -> dict:
    return get_plan_features(PlanNames.PAY_AS_YOU_GO)
