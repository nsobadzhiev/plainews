from litellm import acompletion

from config.config import Config

OLLAMA_BASE = "http://localhost:11434"
config = Config()

async def llm_completion(system_prompt: str, payload: str) -> str:
    response = await acompletion(
        model=_get_llm_model(),
        messages=_get_messages(system_prompt, payload),
        api_base=OLLAMA_BASE,
    )
    return response.choices[0].message.content


def _get_llm_model() -> str:
    return config.llm_model


def _get_messages(system_prompt: str, payload: str) -> list[dict]:
    return [
        {"content": system_prompt, "role": "system"},
        {"content": payload, "role": "user"}
    ]
