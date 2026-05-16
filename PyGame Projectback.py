import pygame as pg
import random as rd
import json

FPS = 90
WIDTH, HEIGHT = 1344, 864
BLACK = (0, 0, 0)
SLOT_1 = (((10 + 0) * 64 + 34), 0 + 37)
SLOT_2 = (((10 + 1) * 64 + 34), 0 + 37)
SLOT_3 = (((10 + 2) * 64 + 34), 0 + 37)
SLOT_4 = (((10 + 3) * 64 + 34), 0 + 37)
SLOT_5 = (((10 + 4) * 64 + 34), 0 + 37)
SLOT_6 = (((10 + 5) * 64 + 34), 0 + 37)
SLOT_7 = (((10 + 6) * 64 + 34), 0 + 37)
SLOT_8 = (((10 + 7) * 64 + 34), 0 + 37)
SLOT_9 = (((10 + 8) * 64 + 34), 0 + 37)
SLOT_10 = (((10 + 9) * 64 + 34), 0 + 37)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Игра")
pg.display.set_icon(pg.image.load("icon.png"))
clock = pg.time.Clock()


class Player:
    COLOR = (0, 0, 255)
    WIDTH, HEIGHT = 50, 50
    SPEED = 5

    def __init__(self):
        self.surf = pg.image.load("Images/Animals/cow_w.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(rd.randint(144, 788), rd.randint(144, 788)))
        self.iteration = 0
        self.animation_number = 1
        self.animation_word = "w"
        self.par = (0, 0)
        self.surf = pg.Surface((Player.WIDTH, Player.HEIGHT), pg.SRCALPHA)
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.speed = Player.SPEED
        self.mask = pg.mask.from_surface(self.surf)
        self.surf.fill((0, 0, 0, 0))
        self.flag = True
        pg.draw.circle(self.surf, (*Player.COLOR, 255),
                       (self.rect.width / 2, self.rect.height / 2), 30)

    def flag_change(self, name):
        self.flag = name

    def move(self, dx=0, dy=0):
        if self.flag:
            if (self.rect.left + dx * self.speed) > 60 and (self.rect.right + dx * self.speed) < WIDTH - 60:
                self.rect.x += dx * self.speed
            if (self.rect.top + dy * self.speed) > 60 and (self.rect.bottom + dy * self.speed) < HEIGHT - 60:
                self.rect.y += dy * self.speed
            match dx, dy:
                case 1, 0:
                    self.animation_word = "d"
                    self.iteration += 1
                case -1, 0:
                    self.animation_word = "a"
                    self.iteration += 1
                case 0, 1:
                    self.animation_word = "s"
                    self.iteration += 1
                case 0, -1:
                    self.animation_word = "w"
                    self.iteration += 1
                case 0, 0:
                    self.animation_number = 1

    def move_predict(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def draw(self):
        self.surf = pg.image.load(
            f"Images/Player/player_{self.animation_word}{str(self.animation_number)}.png").convert_alpha()
        self.surf = pg.transform.scale(self.surf, (80, 80))
        screen.blit(self.surf, self.rect)
        if self.iteration > 8:
            match self.animation_number:
                case 3:
                    self.animation_number = 2
                case 2:
                    self.animation_number = 3
                case 1:
                    self.animation_number = 2
            self.iteration = 0


class Cow:
    def __init__(self):
        self.surf = pg.image.load("Images/Animals/cow_w.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.speed = 2
        self.iteration = 0
        self.iteration_par = rd.randint(80, 220)
        self.flag = True
        self.par = (0, 0)
        # pg.draw.polygon(self.surf, (255, 255, 0), [(0, 0), (self.rect.x, 0), (self.rect.x, self.rect.y), (0, self.rect.y)], 0)

    def draw(self):
        screen.blit(self.surf, self.rect)

    def script(self):
        self.move(*self.par)
        if self.iteration == 60:
            self.par = (0, 0)
        if self.iteration > self.iteration_par:
            par = rd.randint(0, 10)
            match par:
                case 0, 2, 4, 6, 8:
                    self.par = (0, 0)
                case 1:
                    self.surf = pg.image.load("Images/Animals/cow_d.png").convert_alpha()
                    self.move(1)
                    self.par = (1, 0)
                case 3:
                    self.surf = pg.image.load("Images/Animals/cow_a.png").convert_alpha()
                    self.move(-1)
                    self.par = (-1, 0)
                case 5:
                    self.surf = pg.image.load("Images/Animals/cow_w.png").convert_alpha()
                    self.move(0, 1)
                    self.par = (0, 1)
                case 7:
                    self.surf = pg.image.load("Images/Animals/cow_s.png").convert_alpha()
                    self.move(0, -1)
                    self.par = (0, -1)
                case 9:
                    self.surf = pg.image.load("Images/Animals/cow_d.png").convert_alpha()
                    self.move(1.5, 1)
                    self.par = (1.5, 1)
                case 10:
                    self.surf = pg.image.load("Images/Animals/cow_a.png").convert_alpha()
                    self.move(-1.5, -1)
                    self.par = (-1.5, -1)
            self.iteration = 0
        self.iteration += 1

    def move(self, dx=0, dy=0):
        if self.flag:
            if (self.rect.left + dx * self.speed) > 60 and (self.rect.right + dx * self.speed) < WIDTH - 60:
                self.rect.x += dx * self.speed
            if (self.rect.top + dy * self.speed) > 60 and (self.rect.bottom + dy * self.speed) < HEIGHT - 60:
                self.rect.y += dy * self.speed

    def feed(self):
        wheat_item.use(1)
        milk_item.add(1)


class Butterfly:
    def __init__(self, mark):
        self.surf = pg.image.load("Images/Animals/cow_w.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(rd.randint(144, 788), rd.randint(144, 788)))
        self.speed = 2
        self.iteration = 0
        self.background_mark = mark
        self.iteration_par = rd.randint(80, 220)
        self.flag = True
        self.animation_number = 1
        self.animation_word = "w"
        self.par = (0, 0)
        # pg.draw.polygon(self.surf, (255, 255, 0), [(0, 0), (self.rect.x, 0), (self.rect.x, self.rect.y), (0, self.rect.y)], 0)

    def draw(self, mark):
        if self.background_mark == mark:
            self.surf = pg.image.load(
                f"Images/Animals/butterfly/butterfly_{self.animation_word}{str(self.animation_number)}.png").convert_alpha()
            screen.blit(self.surf, self.rect)
        if self.iteration % 10 == 0:
            match self.animation_number:
                case 2:
                    self.animation_number = 1
                case 1:
                    self.animation_number = 2
        self.iteration += 1

    def script(self):
        self.move(*self.par)
        if self.iteration == 60:
            self.par = (0, 0)
        if self.iteration > self.iteration_par:
            par = rd.randint(1, 4)
            match par:
                case 1:
                    self.animation_word = "w"
                    self.move(0, 1)
                    self.par = (0, 1)
                case 2:
                    self.animation_word = "s"
                    self.move(0, -1)
                    self.par = (0, -1)
                case 3:
                    self.animation_word = "d"
                    self.move(1)
                    self.par = (1, 0)
                case 4:
                    self.animation_word = "a"
                    self.move(-1)
                    self.par = (-1, 0)
            self.iteration = 0

    def move(self, dx=0, dy=0):
        if self.flag:
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def check(self):
        if 0 > self.rect.x > 1344:
            self.flag = False
        if 0 > self.rect.y > 864:
            self.flag = False

    def is_active(self):
        return self.flag

class Herb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = True
        self.thirst = False
        self.flag = False
        # self.surf = pg.image.load("path").convert_alpha()
        self.surf_icon = pg.image.load("Images/Icons/Thirst_icon_full.png").convert_alpha()
        # self.rect = self.surf.get_rect(center=(self.x, self.y))
        # self.rect_icon = self.rect
        self.stage = 1
        self.iter_counter = 0

    def draw(self):
        screen.blit(self.surf, self.rect)
        if not self.thirst and self.status or self.flag and self.status:
            screen.blit(self.surf_icon, self.rect_icon)

    def grown(self):
        self.surf_icon.fill((0, 0, 0))
        self.surf_icon = pg.image.load("Images/Icons/Crop_icon_full.png").convert_alpha()

    def irrigation(self):
        self.thirst = True
        if not self.flag:
            self.surf_icon.fill((0, 0, 0))

    def drying_out(self):
        if not self.flag:
            self.thirst = False
            self.surf_icon = pg.image.load("Images/Icons/Thirst_icon_full.png").convert_alpha()

    def check_alive(self):
        return self.status

    def coordinate_x(self):
        return self.x

    def coordinate_y(self):
        return self.y


class Potato(Herb):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pg.image.load("Images/Potato/Potato_first.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.rect_icon = self.rect

    def grow(self):
        if self.iter_counter > 120 and self.thirst and self.stage < 6:
            if self.thirst:
                match self.stage:
                    case 1:
                        self.surf = pg.image.load("Images/Potato/Potato_second.png")
                        self.drying_out()
                    case 2:
                        self.surf = pg.image.load("Images/Potato/Potato_third.png")
                        self.drying_out()
                    case 3:
                        self.surf = pg.image.load("Images/Potato/Potato_premax.png")
                        self.drying_out()
                    case 4:
                        self.surf = pg.image.load("Images/Potato/Potato_max.png")
                        self.flag = True
            self.rect = self.surf.get_rect(center=(self.x, self.y))
            self.iter_counter = 0
            self.stage += 1
            if self.flag:
                self.grown()
            if self.stage != 5:
                self.drying_out()
        elif not self.thirst:
            self.iter_counter = 0
        self.iter_counter += 1

    def crop(self):
        if self.flag and self.status:
            self.surf.fill((0, 0, 0, 0))
            self.surf_icon.fill((0, 0, 0, 0))
            if rd.randint(0, 2) == 1:
                potato_item.add(1)
                potato_seed.add(1)
            else:
                potato_item.add(2)
            self.status = False


class Wheat(Herb):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.surf = pg.image.load("Images/Wheat/Wheat_first.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.rect_icon = self.rect

    def grow(self):
        if self.iter_counter > 120 and self.thirst and self.stage < 6:
            if self.thirst:
                match self.stage:
                    case 1:
                        self.surf = pg.image.load("Images/Wheat/Wheat_second.png")
                        self.drying_out()
                    case 2:
                        self.surf = pg.image.load("Images/Wheat/Wheat_third.png")
                        self.drying_out()
                    case 3:
                        self.surf = pg.image.load("Images/Wheat/Wheat_premax.png")
                        self.drying_out()
                    case 4:
                        self.surf = pg.image.load("Images/Wheat/Wheat_max.png")
                        self.flag = True
            self.rect = self.surf.get_rect(center=(self.x, self.y))
            self.iter_counter = 0
            self.stage += 1
            if self.flag:
                self.grown()
            if self.stage != 5:
                self.drying_out()
        elif not self.thirst:
            self.iter_counter = 0
        self.iter_counter += 1

    def crop(self):
        if self.flag and self.status:
            self.surf.fill((0, 0, 0, 0))
            self.surf_icon.fill((0, 0, 0, 0))
            if rd.randint(0, 2) == 1:
                wheat_item.add(1)
                wheat_seed.add(1)
            else:
                wheat_item.add(2)
            self.status = False


class Inventory:
    def __init__(self):
        self.picked = 0
        self.surf = pg.image.load("Images/Inventory_bar.png")
        self.rect = self.surf.get_rect(center=(WIDTH // 2, 0 + 34))
        self.surf_picked = pg.image.load("Images/inventory_slot_picked.png")
        self.surf_item = pg.image.load("Images/Wheat/Wheat_seed.png")
        self.rect_item = self.surf.get_rect(centerx=((10 + self.picked) * 64 + 34))
        self.rect_picked = self.surf.get_rect(centerx=((10 + self.picked) * 64 + 34))
        self.info_rode = False
        self.picked = 1
        with open('data.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def draw(self):
        screen.blit(self.surf, self.rect)
        self.rect_picked = self.surf.get_rect(centerx=((10 + self.picked) * 64 + 34))
        # self.surf_item = self.surf.get_rect(centerx=((10 + 1) * 64 + 67))
        screen.blit(self.surf_picked, self.rect_picked)
        # screen.blit(self.surf_item, self.rect_item)

    def change(self, number):
        self.picked = number
        self.info_rode = False
        if not self.info_rode:
            for info in self.data:
                try:
                    print(info[f"{str(self.picked + 1)}name"])
                    print(info[f"{str(self.picked + 1)}description"])
                    self.info_rode = True
                except KeyError:
                    print("уаааа")
    def give_picked(self):
        return self.picked


class Item:
    def __init__(self, path, slot):
        self.path = path
        self.count = 0
        self.slot = slot
        self.surf = pg.image.load(self.path).convert_alpha()
        self.rect = inventory.surf.get_rect(centerx=((10 + slot) * 64 + 34))

    def add(self, number):
        self.count += number

    def use(self, number):
        if self.count - number > -1:
            self.count -= number

    def get_count(self):
        return self.count

    def check(self):
        if self.count == 0:
            self.surf.fill((0, 0, 0, 0))
        if self.count > 0:
            self.surf = pg.image.load(self.path).convert_alpha()

    def draw(self):
        screen.blit(self.surf, self.rect)


class Sprinkler: # БОЖЕ УПАСИ
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.iters = 0
        self.animation_number = 1
        self.surf = pg.image.load(f"Images/Sprinkler/Sprinkler_placed_{str(self.animation_number)}.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.rect_icon = self.rect

    def draw(self):
        if self.iters % 30 == 0:
            match self.animation_number:
                case 1:
                    self.animation_number = 2
                    self.surf = pg.image.load(
                        f"Images/Sprinkler/Sprinkler_placed_{str(self.animation_number)}.png").convert_alpha()
                case 2:
                    self.animation_number = 1
                    self.surf = pg.image.load(
                        f"Images/Sprinkler/Sprinkler_placed_{str(self.animation_number)}.png").convert_alpha()
        screen.blit(self.surf, self.rect)
        self.iters += 1

    def sprink(self):
        if self.iters > 320:
            for i in range(8 + 1):
                x_predict = self.x
                y_predict = self.y
                match i:
                    case 1:
                        x_predict -= 96
                        y_predict -= 96
                    case 2:
                        y_predict -= 96
                    case 3:
                        x_predict += 96
                        y_predict -= 96
                    case 4:
                        x_predict += 96
                    case 5:
                        x_predict += 96
                        y_predict += 96
                    case 6:
                        y_predict += 96
                    case 7:
                        x_predict -= 96
                        y_predict += 96
                    case 8:
                        x_predict -= 96
                for elem in wheat:
                    if x_predict == elem.coordinate_x() and y_predict == elem.coordinate_y():
                        elem.irrigation()
                for elem in potatoes:
                    if x_predict == elem.coordinate_x() and y_predict == elem.coordinate_y():
                        elem.irrigation()
                self.iters = 0

    def coordinate_x(self):
        return self.x

    def coordinate_y(self):
        return self.y


class Seed:
    def __init__(self, path, slot):
        self.path = path
        self.usage = 10
        self.slot = slot
        self.surf = pg.image.load(self.path).convert_alpha()
        self.rect = inventory.surf.get_rect(centerx=((10 + slot) * 64 + 35))
        self.x = (10 + 0) * 64 + 35
        self.y = 0 + 37

    def use(self):
        if self.get_usage() > -1:
            self.usage -= 1

    def get_usage(self):
        return self.usage

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def add(self, number):
        self.usage += number

    def check(self):
        if self.usage == 0:
            self.surf.fill((0, 0, 0, 0))
        if self.usage > 0:
            self.surf = pg.image.load(self.path).convert_alpha()

    def draw(self):
        screen.blit(self.surf, self.rect)


class Shop:

    def __init__(self):
        self.surf = pg.image.load("Images/Icons/Shop_icon.png").convert_alpha()
        self.rect = self.surf.get_rect(centerx=(WIDTH - 64))

    def draw(self):
        screen.blit(self.surf, self.rect)

    class Slot:

        def __init__(self, x, y, sprite, second_sprite, strategy):
            self.surf = pg.image.load("Images/shop_slot.png").convert_alpha()
            self.rect = self.surf.get_rect(center=(x, y + 64))
            self.surf_item = pg.image.load(sprite).convert_alpha()
            self.rect_item = self.surf.get_rect(center=(x + 25, y + 96))
            self.surf_get = pg.image.load(second_sprite).convert_alpha()
            self.rect_get = self.surf.get_rect(center=(x + 230, y + 96))
            self.button = pg.image.load("Images/button.png").convert_alpha()
            self.button_rect = self.button.get_rect(center=(x, y - 32))
            self.strategy = strategy
            self.declaration_timer = 0
            self.buy = True
            self.x = x
            self.y = y

        def redraw(self, state):  # state = True, если курсор на кнопке; state = False, если курсор вне кнопки
            if self.buy or self.declaration_timer == 30:
                if state:
                    self.button = pg.image.load("Images/button_pressed.png").convert_alpha()
                    self.button_rect = self.button.get_rect(center=(self.x, self.y - 32))
                else:
                    self.button = pg.image.load("Images/button.png").convert_alpha()
                    self.button_rect = self.button.get_rect(center=(self.x, self.y - 32))
                self.buy = True
                self.declaration_timer = 0
            else:
                self.button = pg.image.load("Images/button_declined.png").convert_alpha()

        def sell(self):
            match self.strategy:
                case 1:
                    if wheat_item.get_count() > 0:
                        money.add(2)
                        wheat_item.use(1)
                    else:
                        self.buy = False
                case 2:
                    if money.get_usage() > 0:
                        money.remove(1)
                        wheat_seed.add(1)
                    else:
                        self.buy = False
                case 3:
                    if potato_item.get_count() > 0:
                        money.add(4)
                        potato_item.use(1)
                    else:
                        self.buy = False
                case 4:
                    if money.get_usage() > 1:
                        money.remove(2)
                        potato_seed.add(1)
                    else:
                        self.buy = False
                case 5:
                    if milk_item.get_count() > 0:
                        milk_item.use(1)
                        money.add(8)
                    else:
                        self.buy = False
                case 6:
                    if money.get_usage() > 19:
                        money.remove(20)
                        sprinkler_item.add(1)
                    else:
                        self.buy = False

        def draw(self):
            screen.blit(self.surf, self.rect)
            screen.blit(self.surf_item, self.rect_item)
            screen.blit(self.surf_get, self.rect_get)
            screen.blit(self.button, self.button_rect)
            if not self.buy:
                self.declaration_timer += 1


class Money:

    def __init__(self):
        self.usage = 100
        self.surf = pg.image.load("Images/Money/Coin_item.png").convert_alpha()
        self.rect = inventory.surf.get_rect(centerx=((10 + 9) * 64 + 34))
        self.x = (10 + 0) * 64 + 34
        self.y = 0 + 37

    def draw(self):
        screen.blit(self.surf, self.rect)

    def get_usage(self):
        return self.usage

    def check(self):
        if self.usage == 0:
            self.surf.fill((0, 0, 0, 0))
        if self.usage > 0:
            self.surf = pg.image.load("Images/Money/Coin_item.png").convert_alpha()

    def add(self, number):
        self.usage += number

    def remove(self, number):
        if self.get_usage() > -1:
            self.usage -= number


class Text:
    def __init__(self, text, text_size, text_color, text_pos, inventory_true):
        self.text = text
        self.text_color = text_color
        self.font = pg.font.SysFont(None, text_size)
        self.suft = self.font.render(text, False, text_color).convert_alpha()
        if inventory_true:
            self.rect = inventory.surf.get_rect(center=text_pos)
        else:
            self.rect = self.suft.get_rect(center=text_pos)

    def draw(self):
        screen.blit(self.suft, self.rect)

    def delete(self):
        self.suft.fill((0, 0, 0, 0))

    def spawn(self):
        self.suft = self.font.render(self.text, False, self.text_color)


class Cloud:
    def __init__(self, mark):
        self.surf = pg.image.load(f"Images/cloud_{str(rd.randint(1, 10))}.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(-576, rd.randint(0, 844)))
        self.speed = rd.randint(0, 10)
        self.background_mark = mark
        self.flag_active = True

    def draw(self, mark):
        self.script(1)
        if self.background_mark == mark:
            screen.blit(self.surf, self.rect)

    def script(self, dx=0):
        self.rect.x += dx * self.speed

    def check(self):
        if self.rect.left > 1344 and self.background_mark == 1:
            self.background_mark = 2
            self.rect.centerx = -576
        if self.rect.left > 1344 and self.background_mark == 2:
            self.flag_active = False

    def is_active(self):
        return self.flag_active


def check_mouse_on_button(button):
    if button.button_rect.collidepoint(pg.mouse.get_pos()):
        button.redraw(state=True)
    else:
        button.redraw(state=False)


def check_click_on_button(button):
    if button.button_rect.collidepoint(pg.mouse.get_pos()):
        button.sell()


def background_check(mark, surf):
    if mark == 1:
        surf = pg.image.load("Images/background_standardmaps.png")
    else:
        surf = pg.image.load("Images/background.png")
    return surf


def check_collusions(player, animals):
    inds = player.rect.collidelistall([elem.rect for elem in animals])
    try:
        for i in str(inds[0]):
            animals[int(i)].feed()
    except IndexError:
        pass


background_surf = pg.image.load("Images/background_standardmaps.png").convert_alpha()
dark_background_surf = pg.image.load("Images/dark_background.png").convert_alpha()
wheat = []
cords = []
nature = []
crop_available_tiles = [(1, 1), (2, 1), (3, 1), (5, 1), (6, 1), (7, 1), (8, 1), (10, 1), (11, 1), (12, 1),
                        (1, 2), (2, 2), (3, 2), (5, 2), (6, 2), (7, 2), (8, 2), (10, 2), (11, 2), (12, 2),
                        (1, 3), (2, 3), (3, 3), (10, 3), (11, 3), (12, 3),
                        (1, 5), (2, 5), (3, 5), (10, 5), (11, 5), (12, 5),
                        (1, 6), (2, 6), (3, 6), (5, 6), (6, 6), (7, 6), (8, 6), (10, 6), (11, 6), (12, 6),
                        (1, 7), (2, 7), (3, 7), (5, 7), (6, 7), (7, 7), (8, 7), (10, 7), (11, 7), (12, 7)]
potatoes = []
iters = 0
counter = 0
background_mark = 1
nature_iters = 0
shop = Shop()
inventory = Inventory()
money = Money()
money_text = Text(str(money.get_usage()), 32, BLACK, (((10 + 9) * 64 + 34), 0 + 37), True)
slot_1 = shop.Slot((WIDTH / 4), (HEIGHT / 4), "Images/Wheat/Wheat_icon.png", "Images/Money/Coin_icon.png", 1)
slot_1text_second = Text("2", 32, BLACK, ((WIDTH / 4 + 64), HEIGHT / 4 - 64), False)
slot_1text_first = Text("1", 32, BLACK, ((WIDTH / 4 - 136), HEIGHT / 4 - 64), False)
slot_2 = shop.Slot((WIDTH / 4), (HEIGHT - HEIGHT / 2), "Images/Money/Coin_icon.png", "Images/Wheat/Wheat_seed_icon.png",
                   2)
slot_2text_second = Text("4", 32, BLACK, ((WIDTH - WIDTH / 4 + 64), HEIGHT / 4 - 64), False)
slot_2text_first = Text("1", 32, BLACK, ((WIDTH - WIDTH / 4 - 136), HEIGHT / 4 - 64), False)
slot_3 = shop.Slot((WIDTH - WIDTH / 4), (HEIGHT / 4), "Images/Potato/Potato_icon.png", "Images/Money/Coin_icon.png", 3)
slot_3text_first = Text("1", 32, BLACK, ((WIDTH / 4 - 136), HEIGHT - HEIGHT / 2 - 64), False)
slot_3text_second = Text("1", 32, BLACK, ((WIDTH / 4 + 64), HEIGHT - HEIGHT / 2 - 64), False)
slot_4 = shop.Slot((WIDTH - WIDTH / 4), (HEIGHT - HEIGHT / 2), "Images/Money/Coin_icon.png",
                   "Images/Potato/Potato_seed_icon.png", 4)
slot_4text_first = Text("2", 32, BLACK, ((WIDTH - WIDTH / 4 - 136), HEIGHT - HEIGHT / 2 - 64), False)
slot_4text_second = Text("1", 32, BLACK, ((WIDTH - WIDTH / 4 + 64), HEIGHT - HEIGHT / 2 - 64), False)
slot_5 = shop.Slot((WIDTH / 4), (HEIGHT - HEIGHT / 4), "Images/Milk/Milk_icon.png", "Images/Money/Coin_icon.png", 5)
slot_5text_second = Text("8", 32, BLACK, ((WIDTH / 4 + 64), (HEIGHT - HEIGHT / 4 - 64)), False)
slot_5text_first = Text("1", 32, BLACK, ((WIDTH / 4 - 136), (HEIGHT - HEIGHT / 4 - 64)), False)
slot_6 = shop.Slot((WIDTH / 2 + WIDTH / 4), (HEIGHT - HEIGHT / 4), "Images/Money/Coin_icon.png", "Images/Sprinkler/Sprinkler_icon.png", 6)
slot_6text_first = Text("20", 32, BLACK, ((WIDTH / 2 + WIDTH / 4 - 136), HEIGHT - HEIGHT / 4 - 64), False)
slot_6text_second = Text("1", 32, BLACK, ((WIDTH / 2 + WIDTH / 4 + 64), HEIGHT - HEIGHT / 4 - 64), False)
slots = [slot_1, slot_2, slot_3, slot_4, slot_5, slot_6]
inventory_use = []
animals = []
player = Player()
animals.append(Cow())
animals.append(Cow())
animals.append(Cow())
sprinklers = []
wheat_seed = Seed("Images/Wheat/Wheat_seed.png", 0)
potato_seed = Seed("Images/Potato/Potato_seed_item.png", 2)
flag_background = False
shop_text = Text("F", 64, BLACK, (WIDTH - 37, 34), False)
wheat_seed_text = Text(str(wheat_seed.get_usage()), 32, BLACK, SLOT_1, True)
potato_seed_text = Text(str(potato_seed.get_usage()), 32, BLACK, SLOT_3, True)
wheat_item = Item("Images/Wheat/Wheat_produce.png", 1)
potato_item = Item("Images/Potato/Potato_produce.png", 3)
milk_item = Item("Images/Milk/Milk_produce.png", 4)
sprinkler_item = Item("Images/Sprinkler/Sprinkler_item.png", 5)
wheat_item_text = Text(str(wheat_item.get_count()), 32, BLACK, SLOT_2, True)
potato_item_text = Text(str(potato_item.get_count()), 32, BLACK, SLOT_5, True)
milk_item_text = Text(str(milk_item.get_count()), 32, BLACK, SLOT_3, True)
sprinkler_item_text = Text(str(sprinkler_item.get_count()), 32, BLACK, SLOT_6, True)
items = [money, wheat_seed, wheat_item, potato_item, potato_seed, milk_item, sprinkler_item]
background_text = [slot_1text_first, slot_1text_second, slot_2text_first, slot_2text_second, slot_3text_first,
                   slot_3text_second, slot_4text_first, slot_4text_second, slot_5text_first, slot_5text_second,
                   slot_6text_first, slot_6text_second]
texts = [shop_text, wheat_seed_text, wheat_item_text, potato_item_text, potato_seed_text, money_text, milk_item_text,
         sprinkler_item_text]
screen.blit(background_surf, (0, 0))
pg.display.update()

flag_play = True
while flag_play:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            flag_play = False
            break
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for elem in slots:
                check_click_on_button(elem)
            if wheat_item.get_count() > 0:
                wheat_item_text = Text(str(wheat_item.get_count()), 32, BLACK, SLOT_1, True)
            else:
                wheat_item_text.delete()
    if not flag_play:
        break
    if wheat_seed.get_usage() > 0:
        wheat_seed_text = Text(str(wheat_seed.get_usage()), 32, BLACK, SLOT_1, True)
    else:
        wheat_seed_text.delete()
    if wheat_item.get_count() > 0:
        wheat_item_text = Text(str(wheat_item.get_count()), 32, BLACK, SLOT_2, True)
    else:
        wheat_item_text.delete()
    if potato_seed.get_usage() > 0:
        potato_seed_text = Text(str(potato_seed.get_usage()), 32, BLACK, SLOT_3, True)  # Боже помилуй этот код:pry:
    else:
        potato_seed_text.delete()
    if potato_item.get_count() > 0:
        potato_item_text = Text(str(potato_item.get_count()), 32, BLACK, SLOT_4, True)
    else:
        potato_item_text.delete()
    if money.get_usage() > 0:
        money_text = Text(str(money.get_usage()), 32, BLACK, SLOT_10, True)
    else:
        money_text.delete()
    if milk_item.get_count() > 0:
        milk_item_text = Text(str(milk_item.get_count()), 32, BLACK, SLOT_5, True)
    else:
        milk_item_text.delete()
    if sprinkler_item.get_count() > 0:
        sprinkler_item_text = Text(str(sprinkler_item.get_count()), 32, BLACK, SLOT_6, True)
    else:
        sprinkler_item_text.delete()
    texts = [shop_text, wheat_seed_text, wheat_item_text, potato_item_text, potato_seed_text, money_text, milk_item_text, sprinkler_item_text]
    keys = pg.key.get_pressed()
    keys_to_check = [pg.K_w, pg.K_s, pg.K_d, pg.K_a]
    if keys[pg.K_f] and counter == 0 and iters > 40:
        flag_background = True
        counter += 1
        player.flag_change(False)
        iters = 0
    if keys[pg.K_f] and counter == 1 and iters > 80:
        dark_background_surf = pg.image.load("Images/dark_background.png").convert_alpha()
        flag_background = False
        counter = 0
        player.flag_change(True)
        iters = 0
    if flag_background:
        screen.blit(dark_background_surf, (0, 0))
        inventory.draw()
        shop.draw()
        for collection in (items, texts):
            for elem in collection:
                elem.draw()
        milk_item_text.draw()
        for elem in items:
            elem.check()
        for elem in slots:
            check_mouse_on_button(elem)
            elem.draw()
        for elem in background_text:
            elem.spawn()
            elem.draw()
        pg.display.update()
    iters += 1
    nature_iters += 1
    if not flag_background:
        for elem in background_text:
            elem.delete()
        inventory_keys = ((pg.K_1, 0), (pg.K_2, 1), (pg.K_3, 2), (pg.K_4, 3), (pg.K_5, 4), (pg.K_6, 5), (pg.K_7, 6),
                          (pg.K_8, 7), (pg.K_9, 8), (pg.K_0, 9))
        for key, number in inventory_keys:
            if keys[key]:
                inventory.change(number)
        any_pressed = any(keys[key] for key in keys_to_check)
        if not any_pressed:
            player.move()
        if keys[pg.KMOD_NONE]:
            player.move()
        if keys[pg.K_a]:
            player.move(dx=-1)
        if keys[pg.K_d]:
            player.move(dx=1)
        if keys[pg.K_w]:
            player.move(dy=-1)
        if keys[pg.K_s]:
            player.move(dy=1)
        if keys[pg.K_e] and Inventory.give_picked(inventory) == 5 and sprinkler_item.get_count() > 0 and background_mark == 1 and iters > 90:
            flag = True
            for i in range(14):
                if i == player.rect.centerx // 96:
                    x = i * 96 + 48
                    break
            for i in range(7 + 1):
                if i == player.rect.centery // 96:
                    y = i * 96 + 48
                    break
            for collection in (potatoes, wheat, sprinklers):
                for elem in collection:
                    if x == elem.coordinate_x() and y == elem.coordinate_y():
                        flag = False
            if flag:
                sprinkler_item.use(1)
                sprinklers.append(Sprinkler(x, y))
                iters = 0
        if keys[pg.K_e] and iters > 30 and Inventory.give_picked(inventory) == 0 and wheat_seed.get_usage() > 0 and background_mark == 1:
            for i in range(14):
                if i == player.rect.centerx // 96:
                    x = i * 96 + 48
                    break
            for i in range(7 + 1):
                if i == player.rect.centery // 96:
                    y = i * 96 + 48
                    break
            flag = True
            for collection in (potatoes, wheat, sprinklers):
                for elem in collection:
                    if x == elem.coordinate_x() and y == elem.coordinate_y():
                        flag = False
            if flag:
                for elem in crop_available_tiles:
                    if elem[0] == ((x - 48) // 96) and elem[1] == ((y - 48) // 96):
                        wheat.append(Wheat(x, y))
                        wheat_seed.use()
                        break
            iters = 0
        if keys[pg.K_e] and iters > 30 and Inventory.give_picked(inventory) == 2 and potato_seed.get_usage() > 0 and background_mark == 1:
            for i in range(14):
                if i == player.rect.centerx // 96:
                    x = i * 96 + 48
                    break
            for i in range(7 + 1):
                if i == player.rect.centery // 96:
                    y = i * 96 + 48
                    break
            flag = True
            for collection in (potatoes, wheat, sprinklers):
                for elem in collection:
                    if x == elem.coordinate_x() and y == elem.coordinate_y():
                        flag = False
            if flag:
                for elem in crop_available_tiles:
                    if elem[0] == ((x - 48) // 96) and elem[1] == ((y - 48) // 96):
                        potatoes.append(Potato(x, y))
                        potato_seed.use()
                        break
            iters = 0
        if keys[pg.K_SPACE] and iters > 20 and background_mark == 1:
            for i in range(14):
                if i == player.rect.centerx // 96:
                    x = i * 96 + 48
                    break
            for i in range(7 + 1):
                if i == player.rect.centery // 96:
                    y = i * 96 + 48
                    break
            for elem in wheat:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    elem.irrigation()
            for elem in potatoes:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    elem.irrigation()
            iters = 0
        if keys[pg.K_e] and background_mark == 1:
            for i in range(14):
                if i == player.rect.centerx // 96:
                    x = i * 96 + 48
                    break
            for i in range(7 + 1):
                if i == player.rect.centery // 96:
                    y = i * 96 + 48
                    break
            for elem in wheat:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    elem.crop()
            for elem in potatoes:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    elem.crop()
        screen.blit(background_surf, (0, 0))
        match background_mark:
            case 1:
                for animal in animals:
                    animal.script()
                for collection in (wheat, potatoes):
                    for elem in collection:
                        elem.draw()
                        elem.grow()
                    for elem in sprinklers:
                        elem.draw()
                        elem.sprink()
                for i in range(14):
                    if i == player.rect.centerx // 96:
                        x = i * 96
                        break
                for i in range(7 + 1):
                    if i == player.rect.centery // 96:
                        y = i * 96
                        break
                if x == 13 * 96:
                    for i in range(3, 6):
                        if y == i * 96:
                            player.move_predict(136, player.get_y())
                            background_mark = 2
            case 2:
                for animal in animals:
                    animal.script()
                    animal.draw()
                for collection in (wheat, potatoes):
                    for elem in collection:
                        elem.grow()
                    for elem in sprinklers:
                        elem.sprink()
                if keys[pg.K_e] and iters > 70:
                    check_collusions(player, animals)
                    iters = 0
                for i in range(14):
                    if i == player.rect.centerx // 96:
                        x = i * 96
                        break
                for i in range(7 + 1):
                    if i == player.rect.centery // 96:
                        y = i * 96
                        break
                if x == 0 * 96:
                    for i in range(3, 6):
                        if y == i * 96:
                            background_mark = 1
                            player.move_predict(1104, player.get_y())
        if nature_iters % 10000 == 0:
            nature.append(Butterfly(background_mark))
        if nature_iters % 1000 == 0:
            nature.append(Cloud(background_mark))
        shop.draw()
        shop_text.draw()
        for elem in items:
            elem.check()
        milk_item_text.draw()
        player.draw()
        inventory.draw()
        for collection in (items, texts):
            for elem in collection:
                elem.draw()
        for elem in nature:
            elem.draw(background_mark)
            elem.script()
            elem.check()
        background_surf = background_check(background_mark, background_surf)
        wheat = [elem for elem in wheat if elem.check_alive()]
        potatoes = [elem for elem in potatoes if elem.check_alive()]
        nature = [elem for elem in nature if elem.is_active()]
        pg.display.update()
