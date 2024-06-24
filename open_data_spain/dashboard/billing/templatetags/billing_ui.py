from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def check_image(current_plan: str, plan_name: str) -> str:
    txt = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" height="12" width="12" class="me-2 {}"><path d="M23.37.29a1.49,1.49,0,0,0-2.09.34L7.25,20.2,2.56,15.51A1.5,1.5,0,0,0,.44,17.63l5.93,5.94a1.53,1.53,0,0,0,2.28-.19l15.07-21A1.49,1.49,0,0,0,23.37.29Z" style="fill: currentColor"></path></svg>'

    enabled = current_plan == plan_name

    if enabled:
        ret = txt.format("text-white")

    else:
        ret = txt.format("text-primary")

    # mark_safe is required to avoid html escaping
    return mark_safe(ret)


@register.simple_tag
def cross_image(current_plan: str, plan_name: str) -> str:
    txt = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" height="12" width="12" class="me-2 {}"><path d="M14.3,12.18a.24.24,0,0,1,0-.35l9.26-9.27a1.49,1.49,0,0,0,0-2.12,1.51,1.51,0,0,0-2.12,0L12.18,9.7a.25.25,0,0,1-.36,0L2.56.44A1.51,1.51,0,0,0,.44.44a1.49,1.49,0,0,0,0,2.12L9.7,11.83a.24.24,0,0,1,0,.35L.44,21.44a1.49,1.49,0,0,0,0,2.12,1.51,1.51,0,0,0,2.12,0l9.26-9.26a.25.25,0,0,1,.36,0l9.26,9.26a1.51,1.51,0,0,0,2.12,0,1.49,1.49,0,0,0,0-2.12Z" style="fill: currentColor"></path></svg>'

    enabled = current_plan == plan_name

    if enabled:
        ret = txt.format("text-white")

    else:
        ret = txt.format("text-secondary")

    # mark_safe is required to avoid html escaping
    return mark_safe(ret)


@register.simple_tag
def billing_background_color(current_plan: str, plan_name: str) -> str:
    if current_plan == plan_name:
        return "text-bg-primary"

    else:
        return ""


@register.simple_tag
def billing_title_color(current_plan: str, plan_name: str) -> str:
    if current_plan == plan_name:
        return ""

    else:
        return "text-secondary"
