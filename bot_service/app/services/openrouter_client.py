"""
Клиент для общения с OpenRouter API.
"""
import httpx

from app.core.config import settings


class OpenRouterClient:
    """Клиент для внешнего сервиса OpenRouter."""

    def __init__(self):
        self._base_url = settings.openrouter_base_url
        self._api_key = settings.openrouter_api_key
        self._model = settings.openrouter_model
        self._site_url = settings.openrouter_site_url
        self._app_name = settings.openrouter_app_name

    async def ask(self, prompt: str) -> str:
        """Отправляет запрос к LLM и возвращает текст ответа."""
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": self._site_url,
            "X-Title": self._app_name,
            "Content-Type": "application/json",
        }

        body = {
            "model": self._model,
            "messages": [{"role": "user", "content": prompt}],
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                headers=headers,
                json=body,
            )

        if response.status_code != 200:
            raise Exception(f"OpenRouter error {response.status_code}: {response.text}")

        data = response.json()
        return data["choices"][0]["message"]["content"]
