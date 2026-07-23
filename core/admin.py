from django.contrib import admin
from .models import Department, Metric


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'metric_type',
                    'current_value', 'max_limit', 'unit', 'cutoff_date')
    list_filter = ('department', 'metric_type')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'department', 'metric_type', 'unit')
        }),
        ('Valores', {
            'fields': ('current_value', 'max_limit', 'cutoff_date'),
        }),
    )
