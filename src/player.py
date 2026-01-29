import arcade


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("resources/player1.png")
        self.speed = 200  

        self.center_x = 704-24
        self.center_y = 1280-1232+24


    def update(self, delta_time = 1 / 60, keys_pressed=None):
        if keys_pressed is None:
            keys_pressed = set()

        dx, dy = 0, 0
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= self.speed * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += self.speed * delta_time
        if arcade.key.UP in keys_pressed or arcade.key.W in keys_pressed:
            dy += self.speed * delta_time
        if arcade.key.DOWN in keys_pressed or arcade.key.S in keys_pressed:
            dy -= self.speed * delta_time

        if dx != 0 and dy != 0:
            factor = 0.7071
            dx *= factor
            dy *= factor

        self.center_x += dx
        self.center_y += dy