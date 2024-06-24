from django.contrib import admin
from prettyjson import PrettyJSONWidget

from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'expiration_date', 'features')
    formfield_overrides = {
        "features": {'widget': PrettyJSONWidget}
    }
    actions = ['deactivate_plan']

    def deactivate_plan(self, request, queryset):
        queryset.update(active=False)

    deactivate_plan.short_description = 'Deactivate selected plans'
