from level3 import Level3
import arcade
from constants import SCREEN_HEIGHT, SCREEN_WIDTH\


SCREEN_TITLE = "Game"

def main():
    game = Level3(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()  # Запускаем начальную настройку игры
    arcade.run()

if __name__ == "__main__":
    main()