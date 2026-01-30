import math
from constants import TILE_SCALING, CAMERA_LERP, ZOOM_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT
import arcade
from player import Player
from enemy import EnemyKnife
from level2 import Level2


class Level1(arcade.View):
    def __init__(self):
        super().__init__()
        self.keys_pressed = set()

        self.world_camera = arcade.camera.Camera2D()
    
    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        map_name = "resources/level1.tmx"
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        self.wall_list = tile_map.sprite_lists["Walls"]
        self.floor_list = tile_map.sprite_lists["Floor"]
        self.collision_list = tile_map.sprite_lists["Collision"]

        self.player = Player()
        self.player_list.append(self.player)
        self.player.center_x = 96
        self.player.center_y = 20

        enemy1 = EnemyKnife("resources/enemy_knife2.png")
        enemy2 = EnemyKnife("resources/enemy_knife4.png")
        enemy3 = EnemyKnife("resources/enemy_knife2.png")
        enemy1.center_x = 36
        enemy1.center_y = 96
        self.enemy_list.append(enemy1)
        enemy2.center_x = 160
        enemy2.center_y = 176
        self.enemy_list.append(enemy2)
        enemy3.center_x = 36
        enemy3.center_y = 288
        self.enemy_list.append(enemy3)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.collision_list
        )

    def on_show(self):
        # window доступен после показа View — настраиваем камеры
        self.world_camera.position = (self.player.center_x, self.player.center_y)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.world_camera.zoom = ZOOM_LEVEL
        self.floor_list.draw()
        self.wall_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
    
    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update(delta_time, self.keys_pressed)
        
        if len(self.enemy_list) == 0:
            # Уровень пройден
            level2 = Level2()
            level2.setup()
            self.window.show_view(level2)

        for enemy in self.enemy_list:
            is_player_dead = enemy.update_enemy(self.player)

            if is_player_dead:
                # ПЕРЕКЛЮЧАЕМ ОКНО НА РЕСТАРТ
                death_view = GameOverView()
                self.window.show_view(death_view)
                return

            # Проверяем, видит ли враг игрока
            if enemy.check_vision(self.player, self.collision_list):
                enemy.state = "CHASE"
            
            if enemy.state == "CHASE":
                # Бежим к игроку
                enemy.follow_sprite(self.player)
            else:
                # Враг стоит или патрулирует
                enemy.change_x = 0
                enemy.change_y = 0
            
            # ВАЖНО: Обновляем позицию врага и обрабатываем коллизии
            # Для простоты можно использовать move(), но лучше отдельный physics engine
            # Если у вас много врагов, нужен physics_engine для каждого или SimplePhysicsEngine
            enemy.center_x += enemy.change_x * delta_time
            enemy.center_y += enemy.change_y * delta_time
            
            # Простейшая проверка столкновения со стенами (чтобы не проходили сквозь них)
            hit_list = arcade.check_for_collision_with_list(enemy, self.collision_list)
            if hit_list:
                # Откат позиции при ударе о стену (очень примитивно)
                enemy.center_x -= enemy.change_x * delta_time
                enemy.center_y -= enemy.change_y * delta_time
        
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

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Игрок атакует! Передаем список врагов в его метод
            success = self.player.attack(self.enemy_list)


class GameOverView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.ui_camera = arcade.camera.Camera2D()
        self.ui_camera.position = (self.width / 2, self.height / 2)

    def on_show_view(self):
        self.on_show()

    def on_draw(self):
        self.clear()
        self.ui_camera.use()
        arcade.draw_text("ВЫ ПОГИБЛИ", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color.RED, font_size=50, anchor_x="center")
        arcade.draw_text("Нажмите R для рестарта", self.window.width / 2, self.window.height / 2 - 20,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            # Возвращаемся в игру
            game_view = Level1()
            game_view.setup()
            self.window.show_view(game_view)

        if key == arcade.key.F11:
            # Переключение режима
            self.window.set_fullscreen(not self.window.fullscreen)
            # При выходе из полноэкранного режима можно восстановить размер
            if not self.window.fullscreen:
                self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)