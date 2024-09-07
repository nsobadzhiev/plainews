from textual.app import App

from ui.home import HomeScreen


class Plainews(App[None]):

    async def on_mount(self) -> None:
        await self.push_screen(HomeScreen())


if __name__ == '__main__':
    app = Plainews()
    app.run()
