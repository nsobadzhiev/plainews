from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel

from model.article import Article

console = Console()

def present_article(article: Article):
    columns = Columns([Panel(article.text)], title=article.title, align='center')
    console.print(columns)
