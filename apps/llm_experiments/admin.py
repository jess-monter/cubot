from django.contrib import admin

from apps.llm_experiments.models import ModelPrompt


@admin.register(ModelPrompt)
class ModelPromptAdmin(admin.ModelAdmin):
    list_display = ("llm_model", "active", "created_at", "updated_at")
    search_fields = ("llm_model", "description")
    list_filter = ("active",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("llm_model", "prompt", "active", "description")}),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
