from game.core.game_window import GameWindow
from game.views.menu_view import MenuView


def main() -> None:
    window = GameWindow()
    menu_view = MenuView()
    window.show_view(menu_view)
    window.run()


if __name__ == "__main__":
    main()