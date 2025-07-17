from apps.llm_experiments.models import ModelPrompt


def get_active_model_prompt() -> ModelPrompt | None:
    try:
        return ModelPrompt.objects.filter(active=True).first()
    except ModelPrompt.DoesNotExist:
        return None
