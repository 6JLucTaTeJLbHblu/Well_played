import os
import sys
import pygame
import time

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        try:
            image = image.convert()
        except pygame.error:
            pass
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        try:
            image = image.convert_alpha()
        except pygame.error:
            pass
    return image


FPS = 60
tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('object.png'),
    'door': load_image('zakrataya_dver_szhataya.png'),
    'opendoor': load_image('otkrytaya_dver_szhataya.png'),
    'button': load_image('knopka_fon_szhataya.png'),
    'pressedbutton': load_image('knopka_nazhataya_fon_szhataya.png'),
    'restart': load_image('restart_szhaty.png'),
    'pause': load_image('pauza_szhaty.png'),
    'left': load_image('strelka_vlevo_szhataya.png'),
    'down': load_image('strelka_vniz_szhataya.png'),
    'right': load_image('strelka_vpravo_szhataya.png'),
    'up': load_image('strelka_vverkh_szhataya.png')}
letter_and_number_images = {'а': load_image('а.png'), 'б': load_image('б.png'), 'в': load_image('в.png'),
                            'г': load_image('г.png'), 'д': load_image('д.png'), 'е': load_image('е.png'),
                            'ё': load_image('ё.png'), 'ж': load_image('ж.png'), 'з': load_image('з.png'),
                            'и': load_image('и.png'), 'й': load_image('й.png'), 'к': load_image('к.png'),
                            'л': load_image('л.png'), 'м': load_image('м.png'), 'н': load_image('н.png'),
                            'о': load_image('о.png'), 'п': load_image('п.png'), 'р': load_image('р.png'),
                            'с': load_image('с.png'), 'т': load_image('т.png'), 'у': load_image('у.png'),
                            'ф': load_image('ф.png'), 'х': load_image('х.png'), 'ц': load_image('ц.png'),
                            'ш': load_image('ш.png'), 'щ': load_image('щ.png'), 'ъ': load_image('ъ.png'),
                            'ы': load_image('ы.png'), 'ь': load_image('ь.png'), 'э': load_image('э.png'),
                            'ю': load_image('ю.png'), 'я': load_image('я.png'), 'ч': load_image('ч.png'),
                            '1': load_image('1.png'), '2': load_image('2.png'), '3': load_image('3.png'),
                            '4': load_image('4.png'), '5': load_image('5.png'), '6': load_image('6.png'),
                            '7': load_image('7.png'), '8': load_image('8.png'), '9': load_image('9.png')}
level_number_images = {1: load_image('1.png'), 2: load_image('2.png'), 3: load_image('3.png'),
                       4: load_image('4.png'), 5: load_image('5.png'), 6: load_image('6.png'),
                       7: load_image('7.png'), 8: load_image('8.png'), 9: load_image('9.png'),
                       10: load_image('10.png'), 'vopros': load_image('vopros.png')}
KAMEHb = {'level5': load_image('Скала.jpg')}
letter_dict = {}
player_image_jump = pygame.transform.scale(load_image('chelik_prygaet_szhaty.png', 'white'), (36, 80))
player_image_jump1 = pygame.transform.scale(load_image('chelik_prygaet_szhaty.png', 'white'), (36, 80))
player_image_jump_back = pygame.transform.flip(player_image_jump, True, False)
player_image = pygame.transform.scale(load_image('chelik_stoit_szhaty.png', 'white'), (36, 90))
player_image1 = pygame.transform.scale(load_image('chelik_stoit_szhaty.png', 'white'), (36, 90))
player_image_back = pygame.transform.flip(player_image1, True, False)
player_image_run = pygame.transform.scale(load_image('chelik_idyot_szhaty.png', 'white'), (36, 90))
player_image_back_run = pygame.transform.flip(player_image_run, True, False)
tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
tiles_wall_group = pygame.sprite.Group()
tiles_floor_group = pygame.sprite.Group()
tiles_roof_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
opendoor_group = pygame.sprite.Group()
ladder_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
pressed_buttons_group = pygame.sprite.Group()
letter_and_number_group = pygame.sprite.Group()
scala_group = pygame.sprite.Group()
restart_group = pygame.sprite.Group()
pause_group = pygame.sprite.Group()
level_number_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
maxlevel = int(open("data/openedlevels.txt", encoding="utf-8").readline())
levelnum = 0


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(colortext='black'):
    highlighting = False
    pygame.display.set_caption('Well played:)')
    size = width, height = 700, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    intro_text = ["Старт"]
    fon = pygame.transform.scale(load_image('fon.png', 'black'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 215
    string_rendered = font.render(intro_text[0], True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 254
    screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= intro_rect.x and event.pos[1] >= intro_rect.y:
                    if event.pos[0] <= intro_rect.width + intro_rect.x:
                        if event.pos[1] <= intro_rect.height + intro_rect.y:
                            menu()
                            break
            elif event.type == pygame.MOUSEMOTION:
                if event.pos[0] >= intro_rect.x and event.pos[1] >= intro_rect.y and \
                        event.pos[0] <= intro_rect.width + intro_rect.x and \
                        event.pos[1] <= intro_rect.height + intro_rect.y:
                    highlighting = True
                else:
                    highlighting = False
        if highlighting:
            string_rendered = font.render(intro_text[0], True, pygame.Color('gray'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 254
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        else:
            string_rendered = font.render(intro_text[0], True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 254
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        text_coord = 215
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


levels = [load_level('Start.txt'), load_level('level_1.txt'), load_level('level_2.txt'), load_level('level_3.txt'),
          load_level('level_4.txt'), load_level('level_5.txt'), load_level('level_6.txt')]


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        # добавление картинки
        super().__init__(all_sprites)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['wall']
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        # Создание линий, ограничивающих картинки
        self.imagewall = pygame.Surface([1, tile_height - 2])
        self.imageroof = pygame.Surface([tile_width - 2, 1])
        self.imagefloor = pygame.Surface([tile_width - 2, 1])
        # Левая стенка
        self.spritewallleft = pygame.sprite.Sprite()
        self.spritewallleft.rect = self.imagewall.get_rect().move(pos_x, pos_y + 1)
        self.spritewallleft.image = self.imagewall
        tiles_wall_group.add(self.spritewallleft)
        # Правая стенка
        self.spritewallright = pygame.sprite.Sprite()
        self.spritewallright.rect = self.imagewall.get_rect().move(pos_x + tile_width - 1, pos_y + 1)
        self.spritewallright.image = self.imagewall
        tiles_wall_group.add(self.spritewallright)
        # Потолок
        self.spriteroof = pygame.sprite.Sprite()
        self.spriteroof.rect = self.imageroof.get_rect().move(pos_x + 1, pos_y + tile_height)
        self.spriteroof.image = self.imageroof
        tiles_roof_group.add(self.spriteroof)
        # Пол
        self.spritefloor = pygame.sprite.Sprite()
        self.spritefloor.rect = self.imagefloor.get_rect().move(pos_x + 1, pos_y)
        self.spritefloor.image = self.imagefloor
        tiles_floor_group.add(self.spritefloor)


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        # добавление картинки
        super().__init__(door_group, tiles_wall_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['door']
        self.rect = self.image.get_rect().move(pos_x, pos_y - tile_height)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        # добавление картинки
        super().__init__(buttons_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['button']
        self.rect = self.image.get_rect().move(pos_x, pos_y - 4)


class Pressedbutton(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        # добавление картинки
        super().__init__(pressed_buttons_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['pressedbutton']
        self.rect = self.image.get_rect().move(pos_x, pos_y - 3)


class Opendoor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        # добавление картинки
        super().__init__(opendoor_group, tiles_wall_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['opendoor']
        self.rect = self.image.get_rect().move(pos_x, pos_y - tile_height)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(player_group)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x + 20, pos_y + 10)
        player = None


class Object(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        # добавление картинки
        super().__init__(object_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['empty']
        self.rect = self.image.get_rect().move(pos_x, pos_y - tile_height)

class Ladder(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        # добавление картинки
        super().__init__(ladder_group)
        imageladder = pygame.Surface([3, tile_height])
        imageladder.fill((255, 0, 0))
        self.sprite = pygame.sprite.Sprite()
        self.image = imageladder
        self.rect = self.image.get_rect().move(pos_x - 3, pos_y)


class Letter_and_Number(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, letter_or_number):
        super().__init__(letter_and_number_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = letter_and_number_images[letter_or_number]
        self.rect = self.image.get_rect().move(pos_x + 5, pos_y + 5)


class KAMEHHbIu(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(scala_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = KAMEHb['level5']
        self.rect = self.image.get_rect().move(pos_x, pos_y + 5)


class Restart(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(restart_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['restart']
        self.rect = self.image.get_rect().move(pos_x + 10, pos_y + 10)


class Pause(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(pause_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['pause']
        self.rect = self.image.get_rect().move(pos_x + 10, pos_y + 10)


class Level_number(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(level_number_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = level_number_images[image]
        self.rect = self.image.get_rect().move(pos_x + 5, pos_y + 5)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(arrow_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images[image]
        self.rect = self.image.get_rect().move(pos_x + 5, pos_y + 5)


def generate_level(level):
    global letter_dict
    new_player, x, y = None, None, None
    letternum = 1
    letter_dict = {}
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
                # Tile('empty', x * tile_width, y * tile_height)
            elif level[y][x] == '#':
                Tile(x * tile_width, y * tile_height)
            elif level[y][x] == '@':
                # Tile('empty', x * tile_width, y * tile_height)
                new_player = Player(x * tile_width - 5, (y - 1) * tile_height, player_image)
                x1 = x
                y1 = y - 1
            elif level[y][x] == '|':
                Door(x * tile_width, y * tile_height)
                x2 = x * tile_width
                y2 = y * tile_height
            elif level[y][x] == '%':
                Tile(x * tile_width, y * tile_height)
                Ladder(x * tile_width, y * tile_height)
            elif level[y][x] == '*':
                Object(x * tile_width, y * tile_height)
                Tile(x * tile_width, y * tile_height)
            elif level[y][x] == '(':
                Tile(x * tile_width, y * tile_height)
                Button(x * tile_width, y * tile_height)
            elif level[y][x] == '/':
                Letter_and_Number(x * tile_width, y * tile_height, 'а')
                letter_dict['а' + str(letternum)] = letter_and_number_group.sprites()[-1]
                letternum += 1
            elif level[y][x] == '>':
                KAMEHHbIu(x * tile_width, y * tile_height)
            elif level[y][x] == '[':
                Restart(x * tile_width, y * tile_height)
            elif level[y][x] == '=':
                Pause(x * tile_width, y * tile_height)
    letternum = 1
    # print(letter_dict)
    return new_player, x1, y1, x2, y2


def menu():
    global tiles_wall_group
    global tiles_floor_group
    global tiles_roof_group
    global all_sprites
    global player_group
    global door_group
    global opendoor_group
    global levelnum
    global buttons_group
    global ladder_group
    global pressed_buttons_group
    global letter_and_number_group
    global letter_dict
    global scala_group
    global restart_group
    global pause_group
    global level_number_group
    global levelnum
    global maxlevel
    size = width, height = 700, 500
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    fon = pygame.transform.scale(load_image('fon.png', 'white'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    string_rendered = font.render('Уровни', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = (height - 70) // 2 - 150
    intro_rect.x = (width - 255) // 2
    for i in range(10):
        if i < maxlevel:
            Level_number((width - 500) // 2 + 50 * i, (height - 70) // 2 + 50, i + 1)
        else:
            Level_number((width - 500) // 2 + 50 * i, (height - 70) // 2 + 50, 'vopros')
    screen.blit(string_rendered, intro_rect)
    level_number_group.draw(screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(level_number_group)):
                    if level_number_group.sprites()[i].rect.collidepoint(event.pos):
                        levelnum = i + 1
                        level_number_group = pygame.sprite.Group()
                        all_sprites = pygame.sprite.Group()
                        tiles_wall_group = pygame.sprite.Group()
                        tiles_floor_group = pygame.sprite.Group()
                        tiles_roof_group = pygame.sprite.Group()
                        player_group = pygame.sprite.Group()
                        opendoor_group = pygame.sprite.Group()
                        buttons_group = pygame.sprite.Group()
                        ladder_group = pygame.sprite.Group()
                        pressed_buttons_group = pygame.sprite.Group()
                        scala_group = pygame.sprite.Group()
                        restart_group = pygame.sprite.Group()
                        pause_group = pygame.sprite.Group()
                        letter_and_number_group = pygame.sprite.Group()
                        door_group = pygame.sprite.Group()
                        play(levels[levelnum], levelnum)


def pause(size1):
    size = width, height = 700, 500
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    fon = pygame.transform.scale(load_image('fon.png', 'white'), (width, height))
    screen.blit(fon, (0, 0))
    text = ['Меню', 'Продолжить']
    true = True
    rects = []
    for i in text:
        font = pygame.font.Font(None, 100)
        string_rendered = font.render(i, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = (height - 288) // 2
        if i == text[1]:
            intro_rect.top += 150
        intro_rect.x = (width - list(intro_rect)[2]) // 2
        screen.blit(string_rendered, intro_rect)
        rects.append(intro_rect)
    pygame.display.flip()
    while true:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in rects:
                    if i.collidepoint(event.pos):
                        if i == rects[0]:
                            menu()
                        else:
                            true = False
    return size1


def play(level, levelnumber):
    global tiles_wall_group
    global tiles_floor_group
    global tiles_roof_group
    global all_sprites
    global player_group
    global door_group
    global opendoor_group
    global player_image
    global player_image_run
    global levelnum
    global buttons_group
    global ladder_group
    global pressed_buttons_group
    global letter_and_number_group
    global letter_dict
    global scala_group
    global restart_group
    global pause_group
    global maxlevel
    if __name__ == '__main__':
        levelcomplete = False
        jump = False
        go = False
        run = False
        speed = 0
        lastspeed = 0
        pygame.display.set_caption('Well played)')
        size = width, height = len(level[0]) * tile_width, len(level) * tile_height
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        new_player, xlist, ylist, xdoor, ydoor = generate_level(level)
        if levelnumber == 0 or levelnumber == 1 or levelnumber == 2 or levelnumber == 3:
            levelcomplete = True
        elif levelnumber == 3:
            font = pygame.font.Font(None, 100)
            string_rendered = font.render('Клик', True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 216
            intro_rect.x = 315
            screen.blit(string_rendered, intro_rect)
        x = xlist * tile_width
        y = ylist * tile_height
        player_group.draw(screen)
        all_sprites.draw(screen)
        door_group.draw(screen)
        buttons_group.draw(screen)
        letter_and_number_group.draw(screen)
        scala_group.draw(screen)
        restart_group.draw(screen)
        pause_group.draw(screen)
        pygame.display.flip()
        rightgo = 0
        leftgo = 0
        flagjump = 0
        clock.tick(FPS)
        coeffyup = 0.2
        time1 = int(round(time.time() * 1000))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                            speed = 1
                            rightgo = 1
                            go = True
                    elif event.key == pygame.K_a:
                        if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                            speed = -1
                            leftgo = 1
                            go = True
                    elif event.key == pygame.K_SPACE:
                        flagjump = 1
                        jump = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                            rightgo = 0
                            if rightgo == 0 and leftgo == 0:
                                speed = 0
                                go = False
                            elif rightgo == 1:
                                speed = 1
                            elif leftgo == 1:
                                speed = -1
                    elif event.key == pygame.K_a:
                        if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                            leftgo = 0
                            if rightgo == 0 and leftgo == 0:
                                speed = 0
                                go = False
                            elif rightgo == 1:
                                speed = 1
                            elif leftgo == 1:
                                speed = -1
                    elif event.key == pygame.K_SPACE:
                        flagjump = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if levelnum == 3:
                        Tile(event.pos[0], event.pos[1])
                    elif levelnum == 5 and not levelcomplete:
                        used = []
                        for i in range(5):
                            indx = list(letter_dict.keys())[i]
                            if letter_dict[indx].rect.collidepoint(event.pos):
                                lanim = list(letter_and_number_images)
                                num = indx[1]
                                if indx not in used:
                                    letter_and_number_group.remove(letter_dict[indx])
                                    if indx[0] == 'я':
                                        letter_dict[indx] = Letter_and_Number(250 + (int(indx[1]) - 1) * tile_width, 350, 'а')
                                        letter_dict[lanim[0] + num] = letter_dict.pop(indx)
                                    else:
                                        letter_dict[indx] = Letter_and_Number(250 + (int(indx[1]) - 1) * tile_width, 350,
                                                                           lanim[lanim.index(indx[0]) + 1])
                                        letter_dict[lanim[lanim.index(indx[0]) + 1] + num] = letter_dict.pop(indx)
                                used.append(lanim[lanim.index(indx[0]) + 1] + num)
                                if 'с1' in list(letter_dict) and 'к2' in list(letter_dict) and 'а3' in list(letter_dict) and\
                                        'л4' in list(letter_dict) and 'а5' in list(letter_dict):
                                    levelcomplete = True
                                    lanim = []
                                    letter_dict = {}
                                    letter_and_number_group = pygame.sprite.Group()
                                    Tile(250, 350)
                                    Tile(450, 350)
                                    break
                    if restart_group.sprites()[-1].rect.collidepoint(event.pos):
                        all_sprites = pygame.sprite.Group()
                        tiles_wall_group = pygame.sprite.Group()
                        tiles_floor_group = pygame.sprite.Group()
                        tiles_roof_group = pygame.sprite.Group()
                        player_group = pygame.sprite.Group()
                        opendoor_group = pygame.sprite.Group()
                        buttons_group = pygame.sprite.Group()
                        ladder_group = pygame.sprite.Group()
                        pressed_buttons_group = pygame.sprite.Group()
                        scala_group = pygame.sprite.Group()
                        restart_group = pygame.sprite.Group()
                        pause_group = pygame.sprite.Group()
                        if levelnum == 5:
                            letter_and_number_group = pygame.sprite.Group()
                        play(levels[levelnum], levelnum)
                    elif pause_group.sprites()[-1].rect.collidepoint(event.pos):
                        screen = pygame.display.set_mode(pause(size))
                        speed = 0
            if flagjump == 1 and jump == False:
                jump = True
            if go:
                player_group.remove(player_group.sprites()[-1])
                new_player = Player(x, y, player_image)
                if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                    x += speed * 3
                if pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                    y -= 0.2
                    x -= speed * 3
                    player_group.remove(player_group.sprites()[-1])
                    new_player = Player(x, y, player_image)
                    if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_floor_group):
                        y += 0.2
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image)
                        speed = 0
                        go = False
                    else:
                        x += speed * 3
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image)
                if jump == False:
                    y += 1
                    player_group.remove(player_group.sprites()[-1])
                    new_player = Player(x, y, player_image)
                    if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_floor_group):
                        coeffyup = 7
                        jump = True
                    y -= 1
                    player_group.remove(player_group.sprites()[-1])
                    new_player = Player(x, y, player_image)
                lastspeed = speed
            if jump:
                if not pygame.sprite.spritecollideany(player_group.sprites()[-1], ladder_group):
                    y -= 7 - coeffyup
                    coeffyup += 0.2
                    player_group.remove(player_group.sprites()[-1])
                    new_player = Player(x, y, player_image_jump)
                    if pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_roof_group):
                        if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                            y += 7 - coeffyup + 0.2
                            coeffyup = 7
                        else:
                            x -= speed * 3
                            player_group.remove(player_group.sprites()[-1])
                            new_player = Player(x, y, player_image_jump)
                            if pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                                y += 7 - coeffyup + 0.2
                                coeffyup = 7
                            x += speed * 3
                            player_group.remove(player_group.sprites()[-1])
                            new_player = Player(x, y, player_image_jump)
                    elif pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_floor_group):
                        while pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_floor_group):
                            y -= 0.2
                            player_group.remove(player_group.sprites()[-1])
                            new_player = Player(x, y, player_image)
                        coeffyup = 0.2
                        y += 1.2
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image)
                        if pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group) or y % 50 + 36 < 50:
                            jump = False
                        if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_floor_group) and y % 50 + 36 < 50:
                            jump = True
                            coeffyup = 0.2
                        y -= 1.2
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image)
            if levelnum == 4 and pygame.sprite.spritecollideany(player_group.sprites()[-1], buttons_group):
                Pressedbutton(pygame.sprite.spritecollideany(player_group.sprites()[-1], buttons_group).rect[0],
                              pygame.sprite.spritecollideany(player_group.sprites()[-1], buttons_group).rect[1])
                buttons_group.remove(pygame.sprite.spritecollideany(player_group.sprites()[-1], buttons_group))
                if len(pressed_buttons_group) == 4:
                    levelcomplete = True
            if pygame.sprite.spritecollideany(player_group.sprites()[-1], ladder_group):
                jump = False
                if flagjump == 1:
                    y -= 2
                    player_group.remove(player_group.sprites()[-1])
                    new_player = Player(x, y, player_image)
            if y >= 500:
                x = 55
                y = 350
                player_group.remove(player_group.sprites()[-1])
                new_player = Player(x, y, player_image)
                speed = 0
                flagjump = 0
                coeffyup = 0.2
                jump = False
                go = False
            if pygame.sprite.spritecollideany(player_group.sprites()[-1], opendoor_group):
                all_sprites = pygame.sprite.Group()
                tiles_wall_group = pygame.sprite.Group()
                tiles_floor_group = pygame.sprite.Group()
                tiles_roof_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                opendoor_group = pygame.sprite.Group()
                buttons_group = pygame.sprite.Group()
                ladder_group = pygame.sprite.Group()
                pressed_buttons_group = pygame.sprite.Group()
                scala_group = pygame.sprite.Group()
                restart_group = pygame.sprite.Group()
                pause_group = pygame.sprite.Group()
                letter_and_number_group = pygame.sprite.Group()
                if levelnum < 5:
                    levelnum += 1
                    maxlevel = levelnum
                    file = open("data/openedlevels.txt", 'w')
                    file.write(str(maxlevel))
                    file.close()
                    play(levels[levelnum], levelnum)
                else:
                    menu()
            if levelcomplete and len(opendoor_group) == 0:
                Opendoor(xdoor, ydoor)
                door_group.sprites()[-1].kill()
                opendoor_group.draw(screen)
            # Анимация
            time2 = int(round(time.time() * 1000))
            if time2 - time1 > 100:
                time1 = time2
                if go:
                    if not run:
                        if speed == -1:
                            player_image = player_image_back
                        elif speed == 1:
                            player_image = player_image1
                        run = True
                    else:
                        if speed == -1:
                            player_image = player_image_back_run
                        elif speed == 1:
                            player_image = player_image_run
                        run = False
            if not go:
                if lastspeed == 1 or lastspeed == 0:
                    player_image = player_image1
                elif lastspeed == -1:
                    player_image = player_image_back
                player_group.remove(player_group.sprites()[-1])
                new_player = Player(x, y, player_image)
            if jump:
                if go:
                    if speed == 1:
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image_jump)
                    elif speed == -1:
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image_jump_back)
                else:
                    if lastspeed == 1 or lastspeed == 0:
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image_jump)
                    elif lastspeed == -1:
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image_jump_back)
            clock.tick(FPS)
            screen.fill((255, 255, 255))
            if levelnumber == 3:
                font = pygame.font.Font(None, 100)
                string_rendered = font.render('Клик', True, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = 216
                intro_rect.x = 315
                screen.blit(string_rendered, intro_rect)
            pause_group.draw(screen)
            restart_group.draw(screen)
            scala_group.draw(screen)
            player_group.draw(screen)
            all_sprites.draw(screen)
            ladder_group.draw(screen)
            buttons_group.draw(screen)
            opendoor_group.draw(screen)
            door_group.draw(screen)
            pressed_buttons_group.draw(screen)
            letter_and_number_group.draw(screen)
            pygame.display.flip()


start_screen()
