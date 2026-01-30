import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from level1 import Level1
from level2 import Level2
from level3 import Level3


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.buttons = {}

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def on_draw(self):
        self.clear()
        w = self.window.width
        h = self.window.height

        arcade.draw_text("MAIN MENU", w / 2, h * 0.75, arcade.color.WHITE, 64, anchor_x="center")

        btn_w = 360
        btn_h = 70
        x = w / 2
        y1 = h * 0.5
        y2 = h * 0.35

        arcade.draw_rect_filled(arcade.XYWH(x, y1, btn_w, btn_h), arcade.color.DARK_BLUE)
        arcade.draw_text("Выбрать уровень", x, y1, arcade.color.WHITE, 24, anchor_x="center", anchor_y="center")
        arcade.draw_rect_filled(arcade.XYWH(x, y2, btn_w, btn_h), arcade.color.DARK_RED)
        arcade.draw_text("Выйти из игры", x, y2, arcade.color.WHITE, 24, anchor_x="center", anchor_y="center")

        # Запомним области кнопок: left, bottom, right, top
        self.buttons['levels'] = (x - btn_w / 2, y1 - btn_h / 2, x + btn_w / 2, y1 + btn_h / 2)
        self.buttons['quit'] = (x - btn_w / 2, y2 - btn_h / 2, x + btn_w / 2, y2 + btn_h / 2)

    def on_mouse_press(self, x, y, button, modifiers):
        if self._point_in_rect(x, y, self.buttons['levels']):
            lv = LevelSelectView()
            self.window.show_view(lv)
        elif self._point_in_rect(x, y, self.buttons['quit']):
            arcade.close_window()

    def _point_in_rect(self, x, y, rect):
        left, bottom, right, top = rect
        return left <= x <= right and bottom <= y <= top


class LevelSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.buttons = {}

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        w = self.window.width
        h = self.window.height

        arcade.draw_text("Выберите уровень", w / 2, h * 0.75, arcade.color.WHITE, 48, anchor_x="center")

        btn_w = 320
        btn_h = 64
        x = w / 2
        y_start = h * 0.55
        gap = 90

        # Level buttons
        for i, label in enumerate(["Level 1", "Level 2", "Level 3"]):
            y = y_start - i * gap
            arcade.draw_rect_filled(arcade.XYWH(x, y, btn_w, btn_h), arcade.color.DARK_SLATE_BLUE)
            arcade.draw_text(label, x, y, arcade.color.WHITE, 22, anchor_x="center", anchor_y="center")
            self.buttons[f"lvl_{i+1}"] = (x - btn_w / 2, y - btn_h / 2, x + btn_w / 2, y + btn_h / 2)

        # Back button
        y_back = y_start - 3 * gap
        arcade.draw_rect_filled(arcade.XYWH(x, y_back, btn_w, btn_h), arcade.color.GRAY)
        arcade.draw_text("Назад", x, y_back, arcade.color.WHITE, 22, anchor_x="center", anchor_y="center")
        self.buttons['back'] = (x - btn_w / 2, y_back - btn_h / 2, x + btn_w / 2, y_back + btn_h / 2)

    def on_mouse_press(self, x, y, button, modifiers):
        if self._point_in_rect(x, y, self.buttons['lvl_1']):
            level = Level1()
            level.setup()
            self.window.show_view(level)
        elif self._point_in_rect(x, y, self.buttons['lvl_2']):
            level = Level2()
            level.setup()
            self.window.show_view(level)
        elif self._point_in_rect(x, y, self.buttons['lvl_3']):
            level = Level3()
            level.setup()
            self.window.show_view(level)
        elif self._point_in_rect(x, y, self.buttons['back']):
            self.window.show_view(MenuView())

    def _point_in_rect(self, x, y, rect):
        left, bottom, right, top = rect
        return left <= x <= right and bottom <= y <= top
