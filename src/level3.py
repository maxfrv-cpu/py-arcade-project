import arcade
from player import Player

TILE_SCALING = 1.0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1280
SCREEN_TITLE = "Level 3"


class Level3(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.keys_pressed = set()
        

    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        map_name = "resources/level3.tmx"
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)


        self.wall_list = tile_map.sprite_lists["Walls"]
        self.floor_list = tile_map.sprite_lists["Floor"]
        self.collision_list = tile_map.sprite_lists["Collision"]

        self.player = Player()
        self.player_list.append(self.player)


        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.collision_list
        )

    def on_draw(self):
        self.clear()

        self.floor_list.draw()
        self.wall_list.draw()
        self.player_list.draw()


    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update(delta_time, self.keys_pressed)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        
    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


def main():
    game = Level3(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()  # Запускаем начальную настройку игры
    arcade.run()


if __name__ == "__main__":
    main()