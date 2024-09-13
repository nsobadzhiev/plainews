from ai.llm import llm_completion

LANGUAGE_TOKEN = "{language}"
TRANSLATE_PROMPT = f"""
Translate the following text to {LANGUAGE_TOKEN}. Don't paraphrase or change the text in any other way. Keep the 
formatting."""

async def translate_text(text: str, language: str) -> str:
    prompt = TRANSLATE_PROMPT.replace(LANGUAGE_TOKEN, language)
    return await llm_completion(prompt, text)
