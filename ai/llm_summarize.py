from ai.llm import llm_completion

TARGET_LENGTH_TOKEN = "{target_length}"
SUMMARIZE_PROMPT = f"""Summarize the following article. Mention all the important information inside and ignore filler 
information and unrelated information. The summary should be roughly around {TARGET_LENGTH_TOKEN} words"""

async def summarize_text(text: str, target_length: int) -> str:
    prompt = SUMMARIZE_PROMPT.replace(TARGET_LENGTH_TOKEN, str(target_length))
    return await llm_completion(prompt, text)
