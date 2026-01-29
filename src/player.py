import arcade


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("resources/player1.png",)
        self.speed = 200
        self.center_x = 0
        self.center_y = 0
        
        # Направления: 0=вверх, 1=вправо, 2=вниз, 3=влево
        self.direction = 0
        self.textures = [
            arcade.load_texture("resources/player1.png"),  # Вверх
            arcade.load_texture("resources/player2.png"),  # Вправо
            arcade.load_texture("resources/player3.png"),  # Вниз
            arcade.load_texture("resources/player4.png"),  # Влево
        ]

    def update(self, delta_time=1/60, keys_pressed=None):
        if keys_pressed is None:
            keys_pressed = set()

        dx, dy = 0, 0
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= self.speed * delta_time
            self.direction = 3  # Влево
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += self.speed * delta_time
            self.direction = 1  # Вправо
        if arcade.key.UP in keys_pressed or arcade.key.W in keys_pressed:
            dy += self.speed * delta_time
            self.direction = 0  # Вверх
        if arcade.key.DOWN in keys_pressed or arcade.key.S in keys_pressed:
            dy -= self.speed * delta_time
            self.direction = 2  # Вниз

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy
        
        # Обновляем текстуру
        self.texture = self.textures[self.direction]