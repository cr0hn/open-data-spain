from django.contrib import admin

from .models import Cache

@admin.register(Cache)
class CacheAdmin(admin.ModelAdmin):
    list_display = ('key', 'created', 'modified')
    search_fields = ('key',)
    ordering = ('-created',)
    readonly_fields = ('created', 'modified')
    fields = ('key', 'value', 'created', 'modified')
