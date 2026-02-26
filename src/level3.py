import arcade
from player import Player
from enemy import EnemyKnife
from constants import TILE_SCALING, CAMERA_LERP, ZOOM_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT


class Level3(arcade.View):
    def __init__(self):
        super().__init__()
        self.keys_pressed = set()

        self.world_camera = arcade.camera.Camera2D()
        self.ui_camera = arcade.camera.Camera2D()

    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        map_name = "resources/level3.tmx"
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)


        self.wall_list = tile_map.sprite_lists["Walls"]
        self.floor_list = tile_map.sprite_lists["Floor"]
        self.collision_list = tile_map.sprite_lists["Collision"]

        self.player = Player()
        self.player_list.append(self.player)
        self.player.center_x = 704-24
        self.player.center_y = 1280-1232+24

        enemy1 = EnemyKnife("resources/enemy_knife2.png")
        enemy1.center_x = 320
        enemy1.center_y = 160
        self.enemy_list.append(enemy1)

        enemmy2 = EnemyKnife("resources/enemy_knife2.png")
        enemmy2.center_x = 504
        enemmy2.center_y = 272
        self.enemy_list.append(enemmy2)

        enemy3 = EnemyKnife("resources/enemy_knife2.png")
        enemy3.center_x = 128
        enemy3.center_y = 272
        self.enemy_list.append(enemy3)

        enemy4 = EnemyKnife("resources/enemy_knife2.png")
        enemy4.center_x = 128
        enemy4.center_y = 688
        self.enemy_list.append(enemy4)

        enemy5 = EnemyKnife("resources/enemy_knife2.png")
        enemy5.center_x = 240
        enemy5.center_y = 456
        self.enemy_list.append(enemy5)

        enemy6 = EnemyKnife("resources/enemy_knife2.png")
        enemy6.center_x = 416
        enemy6.center_y = 592
        self.enemy_list.append(enemy6)

        enemy7 = EnemyKnife("resources/enemy_knife2.png")
        enemy7.center_x = 80
        enemy7.center_y = 1008
        self.enemy_list.append(enemy7)

        enemy8 = EnemyKnife("resources/enemy_knife2.png")
        enemy8.center_x = 496
        enemy8.center_y = 928
        self.enemy_list.append(enemy8)

        enemy9 = EnemyKnife("resources/enemy_knife2.png")
        enemy9.center_x = 240
        enemy9.center_y = 1168
        self.enemy_list.append(enemy9)

        enemy10 = EnemyKnife("resources/enemy_knife2.png")
        enemy10.center_x = 688
        enemy10.center_y = 1168
        self.enemy_list.append(enemy10)

        enemy11 = EnemyKnife("resources/enemy_knife2.png")
        enemy11.center_x = 688
        enemy11.center_y = 320
        self.enemy_list.append(enemy11)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player, self.collision_list
        )

    def on_show(self):
        self.world_camera.position = (self.player.center_x, self.player.center_y)


    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.world_camera.zoom = ZOOM_LEVEL
        self.floor_list.draw()
        self.wall_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        
        self.ui_camera.use()
        arcade.draw_text(f"Осталось врагов: {len(self.enemy_list)}", 10, self.window.height - 30,
                         arcade.color.WHITE, font_size=16)


    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update(delta_time, self.keys_pressed)

        if len(self.enemy_list) == 0:
            win_view = WinView()
            self.window.show_view(win_view)

        for enemy in self.enemy_list:
            is_player_dead = enemy.update_enemy(self.player)

            if is_player_dead:
                death_view = GameOverView()
                self.window.show_view(death_view)
                return

            if enemy.check_vision(self.player, self.collision_list):
                enemy.state = "CHASE"
            
            if enemy.state == "CHASE":
                enemy.follow_sprite(self.player)
            else:
                enemy.change_x = 0
                enemy.change_y = 0
            
            enemy.center_x += enemy.change_x * delta_time
            enemy.center_y += enemy.change_y * delta_time
            
            hit_list = arcade.check_for_collision_with_list(enemy, self.collision_list)
            if hit_list:
                enemy.center_x -= enemy.change_x * delta_time
                enemy.center_y -= enemy.change_y * delta_time
        
        position = (
            self.player.center_x,
            self.player.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            CAMERA_LERP,
        )

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if key == arcade.key.ESCAPE:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
        elif key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            if not self.window.fullscreen:
                self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
            
            self.world_camera = arcade.camera.Camera2D()
            self.world_camera.zoom = ZOOM_LEVEL
            self.world_camera.position = (self.player.center_x, self.player.center_y)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            success = self.player.attack(self.enemy_list)


class PauseView(arcade.View):
    def __init__(self, level_view):
        super().__init__()
        self.level_view = level_view
        self.buttons = {}
        self.ui_camera = arcade.camera.Camera2D()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.ui_camera = arcade.camera.Camera2D()
        self.ui_camera.position = (self.window.width / 2, self.window.height / 2)

    def on_draw(self):
        self.clear()
        self.ui_camera.use()
        arcade.draw_text("ПАУЗА", self.window.width / 2, self.window.height / 2 + 100,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        btn_w = 280
        btn_h = 60
        x = self.window.width / 2
        y1 = self.window.height / 2
        y2 = self.window.height / 2 - 80
        y3 = self.window.height / 2 - 160

        arcade.draw_rect_filled(arcade.XYWH(x, y1, btn_w, btn_h), arcade.color.DARK_GREEN)
        arcade.draw_text("Продолжить игру", x, y1, arcade.color.WHITE, 20,
                         anchor_x="center", anchor_y="center")
        self.buttons['resume'] = (x - btn_w / 2, y1 - btn_h / 2, x + btn_w / 2, y1 + btn_h / 2)

        arcade.draw_rect_filled(arcade.XYWH(x, y2, btn_w, btn_h), arcade.color.DARK_BLUE)
        arcade.draw_text("Главное меню", x, y2, arcade.color.WHITE, 20,
                         anchor_x="center", anchor_y="center")
        self.buttons['menu'] = (x - btn_w / 2, y2 - btn_h / 2, x + btn_w / 2, y2 + btn_h / 2)

        arcade.draw_rect_filled(arcade.XYWH(x, y3, btn_w, btn_h), arcade.color.DARK_RED)
        arcade.draw_text("Выйти из игры", x, y3, arcade.color.WHITE, 20,
                         anchor_x="center", anchor_y="center")
        self.buttons['quit'] = (x - btn_w / 2, y3 - btn_h / 2, x + btn_w / 2, y3 + btn_h / 2)

    def on_mouse_press(self, x, y, button, modifiers):
        if self._point_in_rect(x, y, self.buttons['resume']):
            self.window.show_view(self.level_view)
        elif self._point_in_rect(x, y, self.buttons['menu']):
            from menu import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)
        elif self._point_in_rect(x, y, self.buttons['quit']):
            arcade.close_window()

    def _point_in_rect(self, x, y, rect):
        left, bottom, right, top = rect
        return left <= x <= right and bottom <= y <= top

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.level_view)


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
        arcade.draw_text("Нажмите M для выхода в главное меню", self.window.width / 2, self.window.height / 2 - 60,
                         arcade.color.YELLOW, font_size=16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            game_view = Level3()
            game_view.setup()
            self.window.show_view(game_view)
        
        if key == arcade.key.M:
            from menu import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)

        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            if not self.window.fullscreen:
                self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)


class WinView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.ui_camera = arcade.camera.Camera2D()
        self.ui_camera.position = (self.width / 2, self.height / 2)

    def on_show_view(self):
        self.on_show()

    def on_draw(self):
        self.clear()
        self.ui_camera.use()
        arcade.draw_text("ВЫ ПОБЕДИЛИ!", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color.GREEN, font_size=50, anchor_x="center")
        arcade.draw_text("Нажмите R для новой игры", self.window.width / 2, self.window.height / 2 - 20,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Нажмите M для главного меню", self.window.width / 2, self.window.height / 2 - 60,
                         arcade.color.YELLOW, font_size=16, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            from level1 import Level1
            game_view = Level1()
            game_view.setup()
            self.window.show_view(game_view)
        
        if key == arcade.key.M:
            from menu import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)

        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
            if not self.window.fullscreen:
                self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)
