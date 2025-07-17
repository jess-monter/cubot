import pytest
from apps.llm_experiments.models import ModelPrompt
from apps.llm_experiments.services import get_active_model_prompt


@pytest.mark.django_db
def test_get_active_model_prompt_returns_active_instance():
    prompt = ModelPrompt.objects.create(
        llm_model="mistral", prompt="You are a helpful assistant.", active=True
    )

    result = get_active_model_prompt()

    assert result is not None
    assert result == prompt
    assert result.active is True


@pytest.mark.django_db
def test_get_active_model_prompt_returns_none_if_not_found():
    ModelPrompt.objects.create(llm_model="mistral", prompt="Ignored prompt.", active=False)

    result = get_active_model_prompt()

    assert result is None
