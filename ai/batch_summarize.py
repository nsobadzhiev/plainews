import asyncio

from ai.llm_summarize import summarize_text


async def summarize_batch(
        texts: list[str],
        target_length: int = 500,
        item_length: int = 75,
        article_separator: str = '. '
) -> str:
    summaries = await asyncio.gather(*[summarize_text(text, item_length) for text in texts])
    return article_separator.join(summaries)
