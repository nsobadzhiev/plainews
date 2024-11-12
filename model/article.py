from pydantic import BaseModel


class Article(BaseModel):
    title: str
    text: str
    url: str
    keywords: list[str]
    image_url: str | None = None
    video_url: str | None = None
    language: str

    def __str__(self) -> str:
        return f"{self.title}: ({self.text[:30]})"
