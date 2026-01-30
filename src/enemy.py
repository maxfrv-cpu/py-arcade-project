import arcade
import math

from constants import ANGRY_ENEMY_SPEED, VIEW_DISTANCE, ENEMY_ATTACK_RANGE

class EnemyKnife(arcade.Sprite):
    def __init__(self, image_file):
        super().__init__(image_file)
        self.speed = ANGRY_ENEMY_SPEED
        self.state = "IDLE"  # Состояния: IDLE, CHASE
        self.view_distance = VIEW_DISTANCE  # Как далеко видит враг

        self.change_x = 0
        self.change_y = 0
        
    def look_at(self, target_x, target_y):
        """Поворачивает спрайт лицом к цели"""
        dy = target_y - self.center_y
        dx = target_x - self.center_x
        angle = math.atan2(dy, dx)
        
        # Конвертируем радианы в градусы и устанавливаем угол
        self.angle = math.degrees(angle)

    def follow_sprite(self, player_sprite):
        """Движение к игроку"""
        self.look_at(player_sprite.center_x, player_sprite.center_y)
        
        # Вычисляем вектор движения
        angle_rad = math.radians(self.angle)
        self.change_x = math.cos(angle_rad) * self.speed
        self.change_y = math.sin(angle_rad) * self.speed

    def check_vision(self, player_sprite, collision_list):
        """
        Проверяет, видит ли враг игрока.
        Возвращает True, если есть прямая видимость и игрок в радиусе.
        """
        # 1. Проверка дистанции (чтобы не видели через всю карту)
        dist = arcade.get_distance_between_sprites(self, player_sprite)
        if dist > self.view_distance:
            return False

        # 2. Raycasting (Проверка стен)
        # arcade.has_line_of_sight проверяет, есть ли препятствия между точками
        has_los = arcade.has_line_of_sight(
            (self.center_x, self.center_y),
            (player_sprite.center_x, player_sprite.center_y),
            collision_list
        )
        
        return has_los
    

    def update_enemy(self, player_sprite):
        """Обновление состояния врага"""
        distance = arcade.get_distance_between_sprites(self, player_sprite)
        
        # Если дистанция меньше 10 пикселей — игрок убит
        if distance <= ENEMY_ATTACK_RANGE:
            return True
        return False