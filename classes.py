from load_image import *


pygame.init()
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
tile_width = tile_height = 50
FPS = 60
letter_dict = {}
player_image_jump = pygame.transform.scale(load_image('chelik_prygaet_szhaty.png', 'white'), (36, 80))
player_image_jump1 = pygame.transform.scale(load_image('chelik_prygaet_szhaty.png', 'white'), (36, 80))
player_image_jump_back = pygame.transform.flip(player_image_jump, True, False)
player_image = pygame.transform.scale(load_image('chelik_stoit_szhaty.png', 'white'), (36, 90))
player_image1 = pygame.transform.scale(load_image('chelik_stoit_szhaty.png', 'white'), (36, 90))
player_image_back = pygame.transform.flip(player_image1, True, False)
player_image_run = pygame.transform.scale(load_image('chelik_idyot_szhaty.png', 'white'), (36, 90))
player_image_back_run = pygame.transform.flip(player_image_run, True, False)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, all_sprites, tiles_wall_group, tiles_floor_group, tiles_roof_group):
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
    def __init__(self, pos_x, pos_y, door_group, tiles_wall_group):
        # добавление картинки
        super().__init__(door_group, tiles_wall_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['door']
        self.rect = self.image.get_rect().move(pos_x, pos_y - tile_height)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, buttons_group):
        # добавление картинки
        super().__init__(buttons_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['button']
        self.rect = self.image.get_rect().move(pos_x, pos_y - 4)


class Pressedbutton(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, pressed_buttons_group):
        # добавление картинки
        super().__init__(pressed_buttons_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['pressedbutton']
        self.rect = self.image.get_rect().move(pos_x, pos_y - 3)


class Opendoor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, opendoor_group):
        # добавление картинки
        super().__init__(opendoor_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['opendoor']
        self.rect = self.image.get_rect().move(pos_x, pos_y - tile_height)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, player_group):
        super().__init__(player_group)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x + 20, pos_y + 10)
        player = None


class Object(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, object_group):
        # добавление картинки
        super().__init__(object_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['empty']
        self.rect = self.image.get_rect().move(pos_x, pos_y - tile_height)

class Ladder(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, ladder_group):
        # добавление картинки
        super().__init__(ladder_group)
        imageladder = pygame.Surface([3, tile_height])
        imageladder.fill((255, 0, 0))
        self.sprite = pygame.sprite.Sprite()
        self.image = imageladder
        self.rect = self.image.get_rect().move(pos_x - 3, pos_y)


class Letter_and_Number(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, letter_or_number, letter_and_number_group):
        super().__init__(letter_and_number_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = letter_and_number_images[letter_or_number]
        self.rect = self.image.get_rect().move(pos_x + 5, pos_y + 5)


class KAMEHHbIu(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, scala_group):
        super().__init__(scala_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = KAMEHb['level5']
        self.rect = self.image.get_rect().move(pos_x, pos_y + 5)


class Restart(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, restart_group):
        super().__init__(restart_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['restart']
        self.rect = self.image.get_rect().move(pos_x + 10, pos_y + 10)


class Pause(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, pause_group):
        super().__init__(pause_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = tile_images['pause']
        self.rect = self.image.get_rect().move(pos_x + 10, pos_y + 10)


class Level_number(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, level_number_group):
        super().__init__(level_number_group)
        self.sprite = pygame.sprite.Sprite()
        self.image = level_number_images[image]
        self.rect = self.image.get_rect().move(pos_x + 5, pos_y + 5)
