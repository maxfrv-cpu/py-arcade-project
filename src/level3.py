import arcade
from player import Player
from constants import TILE_SCALING, CAMERA_LERP, ZOOM_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT


class Level3(arcade.View):
    def __init__(self):
        super().__init__()
        self.keys_pressed = set()

        self.world_camera = arcade.camera.Camera2D()

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
        self.player.center_x = 704-24
        self.player.center_y = 1280-1232+24


        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.collision_list
        )

    def on_show(self):
        # Настраиваем позицию камеры при показе View
        self.world_camera.position = (self.player.center_x, self.player.center_y)


    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.world_camera.zoom = ZOOM_LEVEL
        self.floor_list.draw()
        self.wall_list.draw()
        self.player_list.draw()


    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update(delta_time, self.keys_pressed)

        position = (
            self.player.center_x,
            self.player.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
            self.world_camera.position,
            position,
            CAMERA_LERP,  # Плавность следования камеры
        )

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if key == arcade.key.F11:
            # Переключение режима
            self.window.set_fullscreen(not self.window.fullscreen)
            # При выходе из полноэкранного режима можно восстановить размер
            if not self.window.fullscreen:
                self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
            
            # Пересчитываем камеру после изменения размера
            self.world_camera = arcade.camera.Camera2D()
            self.world_camera.zoom = ZOOM_LEVEL
            self.world_camera.position = (self.player.center_x, self.player.center_y)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
