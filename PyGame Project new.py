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

    def draw(self, ):
        screen.blit(self.surf, self.rect)


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
        self.rect = self.surf.get_rect(center=(WIDTH//2, 0 + 34))
        self.surf_picked = pg.image.load("Images/inventory_slot_picked.png")
        self.surf_item = pg.image.load("Images/Wheat/Wheat_seed.png")
        self.rect_item = self.surf.get_rect(centerx=((10+self.picked) * 64 + 67))
        self.rect_picked = self.surf.get_rect(centerx=((10+self.picked) * 64 + 67))
        self.picked = 1

    def draw(self):
        screen.blit(self.surf, self.rect)
        self.rect_picked = self.surf.get_rect(centerx=((10 + self.picked) * 64 + 67))
        # self.surf_item = self.surf.get_rect(centerx=((10 + 1) * 64 + 67))
        screen.blit(self.surf_picked, self.rect_picked)
        # screen.blit(self.surf_item, self.rect_item)

    def change(self, number):
        self.picked = number

    def give_picked(self):
        return self.picked


class Item:
    def __init__(self, path, slot):
        self.path = path
        self.count = 0
        self.surf = pg.image.load(self.path).convert_alpha()
        self.rect = inventory.surf.get_rect(centerx=((10 + slot) * 64 + 67))

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


class Seed:
    def __init__(self, path, slot):
        self.path = path
        self.usage = 10
        self.surf = pg.image.load(self.path).convert_alpha()
        self.rect = inventory.surf.get_rect(centerx=((10 + slot) * 64 + 67))
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
            self.x = x
            self.y = y

        def redraw(self, state):  # state = True, если курсор на кнопке; state = False, если курсор вне кнопки
            if state:
                self.button = pg.image.load("Images/button_pressed.png").convert_alpha()
                self.button_rect = self.button.get_rect(center=(self.x, self.y - 32))
            else:
                self.button = pg.image.load("Images/button.png").convert_alpha()
                self.button_rect = self.button.get_rect(center=(self.x, self.y -32))

        def sell(self):
            match self.strategy:
                case 1:
                    if wheat_item.get_count() > 0:
                        money.add(2)
                        wheat_item.use(1)
                case 2:
                    if money.get_usage() > 0:
                        money.remove(1)
                        wheat_seed.add(1)
                case 3:
                    if potato_item.get_count() > 0:
                        money.add(4)
                        potato_item.use(1)
                case 4:
                    if money.get_usage() > 0:
                        money.remove(1)
                        potato_seed.add(1)


        def draw(self):
            screen.blit(self.surf, self.rect)
            screen.blit(self.surf_item, self.rect_item)
            screen.blit(self.surf_get, self.rect_get)
            screen.blit(self.button, self.button_rect)


class Money():

    def __init__(self):
        self.usage = 0
        self.surf = pg.image.load("Images/Money/Coin_item.png").convert_alpha()
        self.rect = inventory.surf.get_rect(centerx=((10 + 9) * 64 + 67))
        self.x = (10 + 0) * 64 + 67
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
            self.usage -= 1



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

def check_mouse_on_button(button):
    if button.button_rect.collidepoint(pg.mouse.get_pos()):
        button.redraw(state=True)
    else:
        button.redraw(state=False)


def check_click_on_button(button):
    if button.button_rect.collidepoint(pg.mouse.get_pos()):
        button.sell()


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
money = Money()
money_text = Text(str(money.get_usage()), 32, BLACK, (((10 + 9) * 64 + 67), 0 + 37), True)
slot_1 = shop.Slot((WIDTH/4), (HEIGHT/4), "Images/Wheat/Wheat_icon.png", "Images/Money/Coin_icon.png", 1)
slot_2 = shop.Slot((WIDTH/4), (HEIGHT - HEIGHT/4), "Images/Money/Coin_icon.png", "Images/Wheat/Wheat_seed_icon.png", 2)
slot_3 = shop.Slot((WIDTH - WIDTH/4), (HEIGHT/4), "Images/Potato/Potato_icon.png", "Images/Money/Coin_icon.png", 3)
slot_4 = shop.Slot((WIDTH - WIDTH/4), (HEIGHT - HEIGHT/4), "Images/Money/Coin_icon.png",  "Images/Potato/Potato_seed_icon.png", 4)
slots = [slot_1, slot_2, slot_3, slot_4]
inventory_use = []
player = Player()
wheat_seed = Seed("Images/Wheat/Wheat_seed.png", 0)
potato_seed = Seed("Images/Potato/Potato_seed_item.png", 2)
flag_background = False
shop_text = Text("F", 64, BLACK, (WIDTH - 37, 34), False)
wheat_seed_text = Text(str(wheat_seed.get_usage()), 32, BLACK, (((10 + 0) * 64 + 67), 0 + 37), True)
potato_seed_text = Text(str(potato_seed.get_usage()), 32, BLACK, (((10 + 2) * 64 + 67), 0 + 37), True)
wheat_item = Item("Images/Wheat/Wheat_produce.png", 1)
potato_item = Item("Images/Potato/Potato_produce.png", 3)
wheat_item_text = Text(str(wheat_item.get_count()), 32, BLACK, (((10 + 1) * 64 + 67), 0 + 37), True)
potato_item_text = Text(str(potato_item.get_count()), 32, BLACK, (((10 + 3) * 64 + 67), 0 + 37), True)
pg.display.update()
items = [money, wheat_seed, wheat_item, potato_item, potato_seed]
texts = [shop_text, wheat_seed_text, wheat_item_text, potato_item_text, potato_seed_text, money_text]
screen.blit(background_surf, (0, 0))

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
                wheat_item_text = Text(str(wheat_item.get_count()), 32, BLACK, (((10 + 0) * 64 + 67), 0 + 37), True)
            else:
                wheat_item_text.delete()
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
    if potato_seed.get_usage() > 0:
        potato_seed_text = Text(str(potato_seed.get_usage()), 32, BLACK, (((10 + 2) * 64 + 67), 0 + 37), True)
    else:
        potato_seed_text.delete()
    if potato_item.get_count() > 0:
        potato_item_text = Text(str(potato_item.get_count()), 32, BLACK, (((10 + 3) * 64 + 67), 0 + 37), True)
    else:
        potato_item_text.delete()
    if money.get_usage() > 0:
        money_text = Text(str(money.get_usage()), 32, BLACK, (((10 + 9) * 64 + 67), 0 + 37), True)
    else:
        money_text.delete()
    texts = [shop_text, wheat_seed_text, wheat_item_text, potato_item_text, potato_seed_text, money_text]
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
        inventory.draw()
        shop.draw()
        for elem in items:
            elem.draw()
        for elem in texts:
            elem.draw()
        for elem in items:
            elem.check()
        for elem in slots:
            check_mouse_on_button(elem)
            elem.draw()
        pg.display.update()
    iters += 1
    if not flag_background:
        inventory_keys = ((pg.K_1, 0), (pg.K_2, 1), (pg.K_3, 2), (pg.K_4, 3), (pg.K_5, 4), (pg.K_6, 5), (pg.K_7, 6),
                          (pg.K_8, 7), (pg.K_9, 8), (pg.K_0, 9))
        for key, number in inventory_keys:
            if keys[key]:
                inventory.change(number)
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
            for elem in potatoes:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    flag = False
            if flag:
                for elem in crop_available_tiles:
                    if elem[0] == ((x - 64) // 128) and elem[1] == ((y - 64) // 128):
                        wheat.append(Wheat(x, y))
                        wheat_seed.use()
                        break
            iters = 0
        if keys[pg.K_q] and iters > 30 and Inventory.give_picked(inventory) == 2 and potato_seed.get_usage() > -1:
            for i in range(11):
                if i == player.rect.centerx // 128:
                    x = i * 128 + 64
                    break
            for i in range(7 + 1):
                if i == player.rect.centery // 128:
                    y = i * 128 + 64
                    break
            flag = True
            for elem in potatoes:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    flag = False
            for elem in wheat:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    flag = False
            if flag:
                for elem in crop_available_tiles:
                    if elem[0] == ((x - 64) // 128) and elem[1] == ((y - 64) // 128):
                        potatoes.append(Potato(x, y))
                        potato_seed.use()
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
            for elem in potatoes:
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
            for elem in potatoes:
                if x == elem.coordinate_x() and y == elem.coordinate_y():
                    elem.crop()

        screen.blit(background_surf, (0, 0))
        inventory.draw()
        shop.draw()
        shop_text.draw()
        for elem in items:
            elem.draw()
        for elem in texts:
            elem.draw()
        for elem in wheat:
            elem.draw()
            elem.grow()
        for elem in potatoes:
            elem.draw()
            elem.grow()
        for elem in items:
            elem.check()
        player.draw()
        wheat = [elem for elem in wheat if elem.check_alive()]
        potatoes = [elem for elem in potatoes if elem.check_alive()]
        pg.display.update()