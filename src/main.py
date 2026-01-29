from level3 import Level3
from level1 import Level1
import arcade
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from level2 import Level2


SCREEN_TITLE = "Game"

def main():
    game = Level1(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()  # Запускаем начальную настройку игры
    arcade.run()

if __name__ == "__main__":
    main()