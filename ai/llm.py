from litellm import completion


OLLAMA_BASE = "http://localhost:11434"

def llm_completion(system_prompt: str, payload: str) -> str:
    response = completion(
        model=_get_llm_model(),
        messages=_get_messages(system_prompt, payload),
        api_base=OLLAMA_BASE,
    )
    return response.object


def _get_llm_model() -> str:
    # TODO: read it from config
    return "ollama/llama2"


def _get_messages(system_prompt: str, payload: str) -> list[dict]:
    return [
        {"content": system_prompt, "role": "system"},
        {"content": payload, "role": "user"}
    ]
