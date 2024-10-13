from textual.app import App

from ui.home import HomeScreen


class Plainews(App[None]):

    async def on_mount(self) -> None:
        await self.push_screen(HomeScreen())


def run_app():
    app = Plainews()
    app.run()


if __name__ == '__main__':
    run_app()
