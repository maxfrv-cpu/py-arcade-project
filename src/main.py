import arcade
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from menu import MenuView


SCREEN_TITLE = "Game"

def main():
    # Создаём одно окно (fullscreen по умолчанию) и показываем главное меню
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()