from django.contrib import admin
from .models import (
    Lead,
    Activity,
    LeadScoreRule,
    PipelineStage,
    ConversionRate,
)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'company',
        'status',
        'source',
        'score',
        'assigned_to',
        'created_at',
    )

    list_filter = (
        'status',
        'source',
        'assigned_to',
        'created_at',
    )

    search_fields = (
        'first_name',
        'last_name',
        'email',
        'company',
    )

    ordering = ('-created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        'lead',
        'activity_type',
        'subject',
        'user',
        'due_date',
        'completed',
        'created_at',
    )

    list_filter = (
        'activity_type',
        'completed',
        'created_at',
    )

    search_fields = (
        'subject',
        'description',
        'lead__first_name',
        'lead__last_name',
    )


@admin.register(LeadScoreRule)
class LeadScoreRuleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'field',
        'operator',
        'value',
        'points',
        'is_active',
    )

    list_filter = (
        'is_active',
        'field',
        'operator',
    )

    search_fields = (
        'name',
        'field',
        'value',
    )


@admin.register(PipelineStage)
class PipelineStageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'order',
        'description',
        'color',
    )

    ordering = ('order',)


@admin.register(ConversionRate)
class ConversionRateAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'total_leads',
        'converted_leads',
        'conversion_rate',
    )

    list_filter = ('date',)

    ordering = ('-date',)