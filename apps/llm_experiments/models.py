from django.db import models


class ModelPrompt(models.Model):
    llm_model = models.CharField(max_length=100, unique=True)
    prompt = models.TextField()
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.llm_model} - {'Active' if self.active else 'Inactive'}"

    class Meta:
        verbose_name = "Model Prompt"
        verbose_name_plural = "Model Prompts"
        ordering = ["-created_at"]
