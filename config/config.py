from pydantic_settings import BaseSettings


class Config(BaseSettings):
    llm_model: str = "ollama/llama3.1"
    llm_base_url: str | None = "http://localhost:11434"     # for Ollama
    language: str = "english"
    feeds_file: str = 'feeds.pickle'
    articles_file: str = 'articles.pickle'
    transformers: list[str] = []
    followed_feeds: list[str] = [
        "https://rss.sueddeutsche.de/rss/Topthemen",
        "https://feeds.arstechnica.com/arstechnica/index",
    ]
