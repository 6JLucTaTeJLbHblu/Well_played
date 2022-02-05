from classes import *
from load_level import *
import time

pygame.init()
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
letter_dict = {}
maxlevel = int(open("data/openedlevels.txt", encoding="utf-8").readline())
levelnum = 0
levels = [load_level('Start.txt'), load_level('level_1.txt'), load_level('level_2.txt'), load_level('level_3.txt'),
          load_level('level_4.txt'), load_level('level_5.txt'), load_level('level_6.txt')]


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(colortext='black'):
    highlighting = False
    pygame.display.set_caption('Well played:)')
    size = width, height = 700, 500
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    intro_text = ['Well played)', "Старт"]
    fon = pygame.transform.scale(load_image('fon.png', 'black'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        if line == 'Well played)':
            intro_rect.x = 147
        else:
            intro_rect.x = 254
        text_coord += 115
        screen.blit(string_rendered, intro_rect)
    text_coord = 215
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
            string_rendered = font.render(intro_text[1], True, pygame.Color('gray'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 254
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        else:
            string_rendered = font.render(intro_text[1], True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 254
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        text_coord = 215
        pygame.display.flip()
        clock.tick(FPS)


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
                Tile(x * tile_width, y * tile_height, all_sprites, tiles_wall_group, tiles_floor_group, tiles_roof_group)
            elif level[y][x] == '@':
                new_player = Player(x * tile_width - 5, (y - 1) * tile_height, player_image, player_group)
                x1 = x
                y1 = y - 1
            elif level[y][x] == '|':
                Door(x * tile_width, y * tile_height, door_group, tiles_wall_group)
                x2 = x * tile_width
                y2 = y * tile_height
            elif level[y][x] == '%':
                Tile(x * tile_width, y * tile_height, all_sprites, tiles_wall_group, tiles_floor_group, tiles_roof_group)
                Ladder(x * tile_width, y * tile_height, ladder_group)
            elif level[y][x] == '*':
                Object(x * tile_width, y * tile_height, object_group)
                Tile(x * tile_width, y * tile_height, all_sprites, tiles_wall_group, tiles_floor_group, tiles_roof_group)
            elif level[y][x] == '(':
                Tile(x * tile_width, y * tile_height, all_sprites, tiles_wall_group, tiles_floor_group, tiles_roof_group)
                Button(x * tile_width, y * tile_height, buttons_group)
            elif level[y][x] == '/':
                Letter_and_Number(x * tile_width, y * tile_height, 'а', letter_and_number_group)
                letter_dict['а' + str(letternum)] = letter_and_number_group.sprites()[-1]
                letternum += 1
            elif level[y][x] == '>':
                KAMEHHbIu(x * tile_width, y * tile_height, scala_group)
            elif level[y][x] == '[':
                Restart(x * tile_width, y * tile_height, restart_group)
            elif level[y][x] == '=':
                Pause(x * tile_width, y * tile_height, pause_group)
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
            Level_number((width - 500) // 2 + 50 * i, (height - 70) // 2 + 50, i + 1, level_number_group)
        else:
            Level_number((width - 500) // 2 + 50 * i, (height - 70) // 2 + 50, 'vopros', level_number_group)
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
                        if levelnum > 5:
                            levelnum = 5
                        elif levelnum <= maxlevel:
                            level_number_group = pygame.sprite.Group()
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
                        Tile(event.pos[0], event.pos[1], all_sprites, tiles_wall_group, tiles_floor_group, tiles_roof_group)
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
                                        letter_dict[indx] = Letter_and_Number(250 + (int(indx[1]) - 1) * tile_width, 350, 'а', letter_and_number_group)
                                        letter_dict[lanim[0] + num] = letter_dict.pop(indx)
                                    else:
                                        letter_dict[indx] = Letter_and_Number(250 + (int(indx[1]) - 1) * tile_width, 350,
                                                                           lanim[lanim.index(indx[0]) + 1], letter_and_number_group)
                                        letter_dict[lanim[lanim.index(indx[0]) + 1] + num] = letter_dict.pop(indx)
                                used.append(lanim[lanim.index(indx[0]) + 1] + num)
                                if 'с1' in list(letter_dict) and 'к2' in list(letter_dict) and 'а3' in list(letter_dict) and\
                                        'л4' in list(letter_dict) and 'а5' in list(letter_dict):
                                    levelcomplete = True
                                    lanim = []
                                    letter_dict = {}
                                    letter_and_number_group = pygame.sprite.Group()
                                    Tile(250, 350, all_sprites, tiles_wall_group, tiles_floor_group, tiles_roof_group)
                                    Tile(450, 350, all_sprites, tiles_wall_group, tiles_floor_group, tiles_roof_group)
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
                new_player = Player(x, y, player_image, player_group)
                if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                    x += speed * 3
                if pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                    y -= 0.2
                    x -= speed * 3
                    player_group.remove(player_group.sprites()[-1])
                    new_player = Player(x, y, player_image, player_group)
                    if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_floor_group):
                        y += 0.2
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image, player_group)
                        speed = 0
                        go = False
                    else:
                        x += speed * 3
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image, player_group)
                if jump == False:
                    y += 1
                    player_group.remove(player_group.sprites()[-1])
                    new_player = Player(x, y, player_image, player_group)
                    if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_floor_group):
                        coeffyup = 7
                        jump = True
                    y -= 1
                    player_group.remove(player_group.sprites()[-1])
                    new_player = Player(x, y, player_image, player_group)
                lastspeed = speed
            if jump:
                if not pygame.sprite.spritecollideany(player_group.sprites()[-1], ladder_group):
                    y -= 7 - coeffyup
                    coeffyup += 0.2
                    player_group.remove(player_group.sprites()[-1])
                    new_player = Player(x, y, player_image_jump, player_group)
                    if pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_roof_group):
                        if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                            y += 7 - coeffyup + 0.2
                            coeffyup = 7
                        else:
                            x -= speed * 3
                            player_group.remove(player_group.sprites()[-1])
                            new_player = Player(x, y, player_image_jump, player_group)
                            if pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group):
                                y += 7 - coeffyup + 0.2
                                coeffyup = 7
                            x += speed * 3
                            player_group.remove(player_group.sprites()[-1])
                            new_player = Player(x, y, player_image_jump, player_group)
                    elif pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_floor_group):
                        while pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_floor_group):
                            y -= 0.2
                            player_group.remove(player_group.sprites()[-1])
                            new_player = Player(x, y, player_image, player_group)
                        coeffyup = 0.2
                        y += 1.2
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image, player_group)
                        if pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_wall_group) or y % 50 + 36 < 50:
                            jump = False
                        if not pygame.sprite.spritecollideany(player_group.sprites()[-1], tiles_floor_group) and y % 50 + 36 < 50:
                            jump = True
                            coeffyup = 0.2
                        y -= 1.2
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image, player_group)
            if levelnum == 4 and pygame.sprite.spritecollideany(player_group.sprites()[-1], buttons_group):
                Pressedbutton(pygame.sprite.spritecollideany(player_group.sprites()[-1], buttons_group).rect[0],
                              pygame.sprite.spritecollideany(player_group.sprites()[-1], buttons_group).rect[1], pressed_buttons_group)
                buttons_group.remove(pygame.sprite.spritecollideany(player_group.sprites()[-1], buttons_group))
                if len(pressed_buttons_group) == 4:
                    levelcomplete = True
            if pygame.sprite.spritecollideany(player_group.sprites()[-1], ladder_group):
                jump = False
                if flagjump == 1:
                    y -= 2
                    player_group.remove(player_group.sprites()[-1])
                    new_player = Player(x, y, player_image, player_group)
            if y >= 500:
                x = 55
                y = 350
                if levelnum == 2:
                    y = 450
                player_group.remove(player_group.sprites()[-1])
                new_player = Player(x, y, player_image, player_group)
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
                    if maxlevel < levelnum:
                        maxlevel = levelnum
                        file = open("data/openedlevels.txt", 'w')
                        file.write(str(maxlevel))
                        file.close()
                    play(levels[levelnum], levelnum)
                else:
                    menu()
            if levelcomplete and len(opendoor_group) == 0:
                Opendoor(xdoor, ydoor, opendoor_group)
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
                new_player = Player(x, y, player_image, player_group)
            if jump:
                if go:
                    if speed == 1:
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image_jump, player_group)
                    elif speed == -1:
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image_jump_back, player_group)
                else:
                    if lastspeed == 1 or lastspeed == 0:
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image_jump, player_group)
                    elif lastspeed == -1:
                        player_group.remove(player_group.sprites()[-1])
                        new_player = Player(x, y, player_image_jump_back, player_group)
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
