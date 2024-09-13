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
    # Seems that Ollama gets confused if chat history with different roles is provided. This is
    # probably not the case with more powerful models
    return [
        {"content": system_prompt + '\n\n' + payload, "role": "assistant"},
    ]
    # return [
    #     {"content": system_prompt, "role": "assistant"},
    #     {"content": payload, "role": "user"}
    # ]
