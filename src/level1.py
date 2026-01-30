from constants import TILE_SCALING, CAMERA_LERP, ZOOM_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT
import arcade
from player import Player
from enemy import EnemyKnife

SCREEN_TITLE = "Level 1"
STATE_GAME = 0
STATE_GAME_OVER = 1

class Level1(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)
        self.keys_pressed = set()

        self.world_camera = arcade.camera.Camera2D()
        self.ui_camera = arcade.camera.Camera2D()
    
    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.current_state = STATE_GAME

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

    def on_draw(self):
        self.clear()

        if self.current_state == STATE_GAME:
            self.world_camera.use()
            self.world_camera.zoom = ZOOM_LEVEL
            self.floor_list.draw()
            self.wall_list.draw()
            self.player_list.draw()
            self.enemy_list.draw()

        elif self.current_state == STATE_GAME_OVER:
            # Рисуем экран смерти
            arcade.draw_rect_filled(arcade.XYWH(self.width/2, self.height/2, self.width, self.height), arcade.color.BLACK_BEAN)
            arcade.draw_text("ВЫ ПОГИБЛИ", self.width/2, self.height/2 + 50, 
                             arcade.color.RED, 50, anchor_x="center")
            arcade.draw_text("Нажмите R для рестарта", self.width/2, self.height/2 - 20, 
                             arcade.color.WHITE, 20, anchor_x="center")
            self.ui_camera.use()
    
    def on_update(self, delta_time):
        if self.current_state == STATE_GAME:
            self.physics_engine.update()
            self.player_list.update(delta_time, self.keys_pressed)

            for enemy in self.enemy_list:
                is_player_dead = enemy.update_enemy(self.player)
                if is_player_dead:
                    self.current_state = STATE_GAME_OVER
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
            self.set_fullscreen(not self.fullscreen)
            # При выходе из полноэкранного режима можно восстановить размер
            if not self.fullscreen:
                self.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
            
            # Пересчитываем камеру после изменения размера
            self.world_camera = arcade.camera.Camera2D()
            self.world_camera.zoom = ZOOM_LEVEL
            self.world_camera.position = (self.player.center_x, self.player.center_y)
            self.ui_camera = arcade.camera.Camera2D()
            self.ui_camera.position = (self.width / 2, self.height / 2)

        if self.current_state == STATE_GAME_OVER:
            if key == arcade.key.R:
                # Перезапускаем всё
                self.setup()
    
    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)   
