from ai.llm import llm_completion

LANGUAGE_TOKEN = "{language}"
TRANSLATE_PROMPT = f"""
Translate the following text to {LANGUAGE_TOKEN}
"""

def translate_text(text: str, language: str) -> str:
    prompt = TRANSLATE_PROMPT.replace(LANGUAGE_TOKEN, language)
    return llm_completion(prompt, text)
