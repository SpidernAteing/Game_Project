import pygame as pg
import random as rd
FPS = 60
WIDTH, HEIGHT = 1408, 896
BLACK = (0, 0, 0)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Игра")
pg.display.set_icon(pg.image.load("icon.png"))
clock = pg.time.Clock()


class Player:
    COLOR = (0, 0, 255)
    WIDTH, HEIGHT = 100, 100
    SPEED = 5

    def __init__(self):
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
            if (self.rect.left + dx * self.speed) > 105 and (self.rect.right + dx * self.speed) < WIDTH - 105:
                self.rect.x += dx * self.speed
            if (self.rect.top + dy * self.speed) > 105 and (self.rect.bottom + dy * self.speed) < HEIGHT - 105:
                self.rect.y += dy * self.speed

    def draw(self, screen):
        screen.blit(self.surf, self.rect)


class Potato:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.thirst = False
        self.surf = pg.image.load("Images/Potato/Potato_first.png").convert_alpha()
        self.surf_icon = pg.image.load("Images/Icons/Thirst_icon_full.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.rect_icon = self.rect
        self.stage = 1
        self.iter_counter = 0

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        screen.blit(self.surf_icon, self.rect_icon)

    def grow(self):
        if self.thirst:
            if self.iter_counter > 460:
                if self.stage == 1:
                    self.surf = pg.image.load("Images/Potato/Potato_second.png")
                    self.drying_out()
                if self.stage == 2:
                    self.surf = pg.image.load("Images/Potato/Potato_third.png")
                    self.drying_out()
                if self.stage == 3:
                    self.surf = pg.image.load("Images//Potato/Potato_premax.png")
                    self.drying_out()
                if self.stage == 4:
                    self.surf = pg.image.load("Images//Potato/Potato_max.png")
                self.rect = self.surf.get_rect(center=(self.x, self.y))
                self.stage += 1
                self.iter_counter = 0
            self.iter_counter += 1

    def irrigation(self):
        self.thirst = True
        self.surf_icon.fill((0, 0, 0, 0))

    def drying_out(self):
        self.thirst = False
        self.surf_icon = pg.image.load("Images/Icons/Thirst_icon_full.png").convert_alpha()


class Inventory:
    def __init__(self):
        self.picked = 0
        self.surf = pg.image.load("Images/Inventory_bar.png")
        self.rect = self.surf.get_rect(center=(WIDTH//2, 0 + 34))
        self.surf_picked = pg.image.load("Images/inventory_slot_picked.png")
        self.surf_item = pg.image.load("Images/Wheat/Wheat_seed.png")
        self.rect_item = self.surf.get_rect(centerx=((10+self.picked) * 64 + 67))
        self.rect_picked = self.surf.get_rect(centerx=((10+self.picked) * 64 + 67))
        self.picked = 1

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        self.rect_picked = self.surf.get_rect(centerx=((10 + self.picked) * 64 + 67))
        # self.surf_item = self.surf.get_rect(centerx=((10 + 1) * 64 + 67))
        screen.blit(self.surf_picked, self.rect_picked)
        # screen.blit(self.surf_item, self.rect_item)

    def change(self, number):
        self.picked = number

    def give_picked(self):
        return self.picked


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

    def draw(self, screen):
        screen.blit(self.suft, self.rect)

    def delete(self):
        self.suft.fill((0, 0, 0, 0))

    def spawn(self):
        self.suft = self.font.render(self.text, False, self.text_color)


class Button:
    def __init__(self, text, text_size, text_color, button_color, button_cover_color, button_pos):
        self.button_color = button_color
        self.button_cover_color = button_cover_color
        self.font = pg.font.SysFont(None, text_size)
        # поверхность и Rect текста:
        self.text_surf = self.font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=button_pos)
        # т. к. она прилегает к тексту вплотную, делаем поверхность и Rect кнопки, границы к-рой будут на 50px дальше:
        self.button_surf = pg.Surface((self.text_surf.get_width() + 50, self.text_surf.get_height() + 50))
        self.button_rect = self.button_surf.get_rect(center=button_pos)
        self.button_surf.fill(button_color)
        pg.draw.rect(self.button_surf, BLACK, (0, 0, self.button_rect.width, self.button_rect.height), 3)

    def redraw(self, state):  # state = True, если курсор на кнопке; state = False, если курсор вне кнопки
        if state:
            self.button_surf.fill(self.button_cover_color)
            pg.draw.rect(self.button_surf, BLACK, (0, 0, self.button_rect.width, self.button_rect.height), 3)
        else:
            self.button_surf.fill(self.button_color)
            pg.draw.rect(self.button_surf, BLACK, (0, 0, self.button_rect.width, self.button_rect.height), 3)

    def draw(self, screen):
        screen.blit(self.button_surf, self.button_rect)
        screen.blit(self.text_surf, self.text_rect)


def check_click_on_button(button):
    if button.button_rect.collidepoint(pg.mouse.get_pos()):
        print("Кнопка была нажата!")


class Wheat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = True
        self.thirst = False
        self.flag = False
        self.surf = pg.image.load("Images//Wheat/Wheat_first.png").convert_alpha()
        self.surf_icon = pg.image.load("Images/Icons/Thirst_icon_full.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.rect_icon = self.rect
        self.stage = 1
        self.iter_counter = 0

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        if not self.thirst and self.status or self.flag and self.status:
            screen.blit(self.surf_icon, self.rect_icon)

    def grow(self):
        if self.iter_counter > 120 and self.thirst and self.stage < 6:
            if self.stage == 1 and self.thirst:
                self.surf = pg.image.load("Images/Wheat/Wheat_second.png")
            if self.stage == 2 and self.thirst:
                self.surf = pg.image.load("Images/Wheat/Wheat_third.png")
            if self.stage == 3 and self.thirst:
                self.surf = pg.image.load("Images//Wheat/Wheat_premax.png")
            if self.stage == 4 and self.thirst:
                self.surf = pg.image.load("Images//Wheat/Wheat_max.png")
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

    def grown(self):
        self.surf_icon.fill((0, 0, 0))
        self.surf_icon = pg.image.load("Images/Icons/Crop_icon_full.png").convert_alpha()

    def crop(self):
        if self.flag and self.status:
            self.surf.fill((0, 0, 0, 0))
            self.surf_icon.fill((0, 0, 0, 0))
            if rd.randint(0, 2) == 1:
                wheat_seed.add(2)
                wheat_item.add(1)
            else:
                wheat_seed.add(1)
                wheat_item.add(2)
            self.status = False

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

    class Item:

        def __init__(self):
            self.count = 0
            self.surf = pg.image.load("Images/Wheat/Wheat_produce.png").convert_alpha()
            self.rect = inventory.surf.get_rect(centerx=((10 + 1) * 64 + 67))

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
                self.surf = pg.image.load("Images/Wheat/Wheat_produce.png").convert_alpha()

        def draw(self):
            screen.blit(self.surf, self.rect)

    class Seed:

        def __init__(self):
            self.usage = 10
            self.surf = pg.image.load("Images/Wheat/Wheat_seed.png").convert_alpha()
            self.rect = inventory.surf.get_rect(centerx=((10 + 0) * 64 + 67))
            self.x = (10 + 0) * 64 + 67
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
                self.surf = pg.image.load("Images/Wheat/Wheat_seed.png").convert_alpha()

        def draw(self):
            screen.blit(self.surf, self.rect)


class Shop:

    def __init__(self):
        self.surf = pg.image.load("Images/Icons/Shop_icon.png").convert_alpha()
        self.rect = self.surf.get_rect(centerx=(WIDTH - 64))

    def draw(self):
        screen.blit(self.surf, self.rect)

background_surf = pg.image.load("Images/background.png").convert_alpha()
dark_background_surf = pg.image.load("Images/dark_background.png").convert_alpha()
wheat = []
cords = []
crop_available_tiles = [(1, 1), (2, 1), (3, 1), (7, 1), (8, 1), (9, 1),
                        (1, 2), (2, 2), (3, 2), (7, 2), (8, 2), (9, 2),
                        (1, 4), (2, 4), (3, 4), (7, 4), (8, 4), (9, 4),
                        (1, 5), (2, 5), (3, 5), (7, 5), (8, 5), (9, 5)]
potatoes = []
iters = 0
counter = 0
shop = Shop()
inventory = Inventory()
inventory_use = []
player = Player()
wheat_seed = Wheat.Seed()
flag_background = False
shop_text = Text("F", 64, BLACK, (WIDTH - 37, 34), False)
wheat_seed_text = Text(str(wheat_seed.get_usage()), 32, BLACK, (((10 + 0) * 64 + 67), 0 + 37), True)
wheat_item = Wheat.Item()
wheat_item_text = Text(str(wheat_item.get_count()), 32, BLACK, (((10 + 11) * 64 + 67), 0 + 37), True)
pg.display.update()
screen.blit(background_surf, (0, 0))

flag_play = True
while flag_play:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            flag_play = False
            break
    if not flag_play:
        break
    if wheat_seed.get_usage() > 0:
        wheat_seed_text = Text(str(wheat_seed.get_usage()), 32, BLACK, (((10 + 0) * 64 + 67), 0 + 37), True)
    else:
        wheat_seed_text.delete()
    if wheat_item.get_count() > 0:
        wheat_item_text = Text(str(wheat_item.get_count()), 32, BLACK, (((10 + 1) * 64 + 67), 0 + 37), True)
    else:
        wheat_item_text.delete()
    keys = pg.key.get_pressed()
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
        pg.display.update()
    iters += 1
    if not flag_background:
        if keys[pg.K_1]:
            inventory.change(0)
        if keys[pg.K_2]:
            inventory.change(1)
        if keys[pg.K_3]:
            inventory.change(2)
        if keys[pg.K_4]:
            inventory.change(3)
        if keys[pg.K_5]:
            inventory.change(4)
        if keys[pg.K_6]:
            inventory.change(5)
        if keys[pg.K_7]:
            inventory.change(6)
        if keys[pg.K_8]:
            inventory.change(7)
        if keys[pg.K_9]:
            inventory.change(8)
        if keys[pg.K_0]:
            inventory.change(9)
        if keys[pg.K_a]:
            player.move(dx=-1)
        if keys[pg.K_d]:
            player.move(dx=1)
        if keys[pg.K_w]:
            player.move(dy=-1)
        if keys[pg.K_s]:
            player.move(dy=1)
        if keys[pg.K_q] and iters > 30 and Inventory.give_picked(inventory) == 0 and wheat_seed.get_usage() > -1:
            for i in range(11):
                if i == player.rect.centerx // 128:
                    x = i * 128 + 64
                    break
            for i in range(7 + 1):
                if i == player.rect.centery // 128:
                    y = i * 128 + 64
                    break
            flag = True
            for elem in wheat:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    flag = False
            if flag:
                for elem in crop_available_tiles:
                    if elem[0] == ((x - 64) // 128) and elem[1] == ((y - 64) // 128):
                        wheat.append(Wheat(x, y))
                        wheat_seed.use()
                        break
            iters = 0
        if keys[pg.K_SPACE] and iters > 15:
            for i in range(11):
                if i == player.rect.centerx // 128:
                    x = i * 128 + 64
                    break
            for i in range(7 + 1):
                if i == player.rect.centery // 128:
                    y = i * 128 + 64
                    break
            for elem in wheat:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    elem.irrigation()
            iters = 0
        if keys[pg.K_e]:
            for i in range(11):
                if i == player.rect.centerx // 128:
                    x = i * 128 + 64
                    break
            for i in range(7 + 1):
                if i == player.rect.centery // 128:
                    y = i * 128 + 64
                    break
            for elem in wheat:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    elem.crop()

        screen.blit(background_surf, (0, 0))
        inventory.draw(screen)
        shop.draw()
        shop_text.draw(screen)
        wheat_item.draw()
        wheat_item_text.draw(screen)
        wheat_seed.draw()
        wheat_seed_text.draw(screen)
        for elem in wheat:
            elem.draw(screen)
            elem.grow()
        player.draw(screen)
        wheat_item.check()
        wheat_seed.check()
        wheat = [elem for elem in wheat if elem.check_alive()]
        pg.display.update()