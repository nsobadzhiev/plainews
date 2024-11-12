from textual import on
from textual.app import App

from ui.feeds_list import FeedsList
from ui.home import HomeScreen
from ui.latest_articles_screen import LatestArticlesScreen


class Plainews(App[None]):

    async def on_mount(self) -> None:
        await self.push_screen(HomeScreen())

    @on(FeedsList.PushLatestArticles)
    def on_push_latest_articles(self, push_event: FeedsList.PushLatestArticles):
        articles_screen = LatestArticlesScreen()
        self.push_screen(articles_screen)


def run_app():
    app = Plainews()
    app.run()


if __name__ == '__main__':
    run_app()
