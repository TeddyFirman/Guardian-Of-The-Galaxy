import pygame
import sys
import time
import random

from models.ship import Player, Enemy, Obstacle, Player2, Repair
# from models.meteor import Obstacle
from models.explosion import Explosion, explosion_group
from models.controls import audio_cfg, display_cfg
from models.scores import scores
from models.icon_button import IconButton
from utils.collide import collide
from utils.assets import Assets
from .background import bg_obj

from config import config
from constants import Path, Image, Font, Colors

pause = False

play_btn = IconButton(Image.PLAY_IMAGE)


def game(isMouse=False):
    global pause
    lives = 5
    laser_vel = 10

    sub_font = pygame.font.Font(Font.neue_font, 40)
    sub_small_font = pygame.font.Font(Font.neue_font, 35)
    pop_up_font = pygame.font.Font(Font.edit_undo_font, 55)

    # load and play ingame music
    audio_cfg.play_music(Path.GAME_MUSIC_PATH)

    enemies = []
    wave_length = 0
    enemy_vel = 1

    # obstacle
    obstacles = []
    wave_length_obs = 0
    obs_vel = 1

    # heal
    heals = []
    wave_length_heal= 0
    heal_vel = 1

    player = Player(config.center_x, 585, mouse_movement=isMouse)
    if isMouse == True:
        pygame.mouse.set_visible(False)
    elif isMouse == False:
        pygame.mouse.set_visible(True)

    lost = False
    win = False
    boss_entry = True

    pause_btn = IconButton(Image.PAUSE_IMAGE)

    explosion_group.empty()

    def redraw_window():
        bg_obj.update()
        bg_obj.render()

        player.draw()

        for enemyShip in enemies:
            enemyShip.draw()

        if pause == True:
            play_btn.draw((config.center_x, 45), True, True)
        else:
            pause_btn.draw((config.center_x, 45), True, True)

        # Lives
        for index in range(1, lives + 1):
            Assets.image.draw(Image.HEART_IMAGE,
                              (config.starting_x + 37 * index - 7, 30))

        # Draw Text
        Assets.text.draw(f'{player.get_level()} / 10', sub_small_font, Colors.CYAN,
                         (config.starting_x + 33, 75))

        score = player.get_score()
        leftScoreIdx = 0
        if score >= 100 and score < 1000:
            leftScoreIdx = 1
        elif score >= 1000:
            leftScoreIdx = 2

        score_label = Assets.text.render(
            f'{score}', sub_font, Colors.GREEN)
        Assets.text.drawSurface(
            score_label, (config.ending_x - score_label.get_width() - 30, 20))
        Assets.image.draw(Image.STAR_IMAGE,
                          (config.ending_x - Image.SKULL_IMAGE.get_width() - 85 - leftScoreIdx*23, 26))

        kills = player.get_kills()
        leftKillsIdx = 0
        if kills >= 100:
            leftKillsIdx = 1

        Assets.image.draw(Image.SKULL_IMAGE,
                          (config.ending_x - Image.SKULL_IMAGE.get_width() - 85 - leftKillsIdx*15, 82))
        kills_label = Assets.text.render(
            f'{kills}', sub_font, Colors.RED)
        Assets.text.drawSurface(
            kills_label, (config.ending_x - kills_label.get_width() - 30, 75))

        if win:
            scores.append(True, player.get_level(), player.get_score(), player.get_kills())
            Assets.text.draw('WINNER :)', pop_up_font, Colors.GREEN,
                             (config.center_x, 350), True)

        if lost:
            scores.append(False, player.get_level(), player.get_score(), player.get_kills())
            Assets.text.draw('GAME OVER :(', pop_up_font, Colors.RED,
                             (config.center_x, 350), True)

        if player.get_level() >= 10 and boss_entry:
            Assets.text.draw('BOSS LEVEL!!', pop_up_font, Colors.RED,
                             (config.center_x, 350), True)

        # explosion group
        explosion_group.draw(config.CANVAS)
        explosion_group.update()

        audio_cfg.display_volume()
        pygame.display.flip()
        config.clock.tick(config.FPS)

    while player.run:
        redraw_window()
        if lives > 0:
            if player.health <= 0:
                lives -= 1
                player.health = 100
        else:
            lost = True
            redraw_window()
            time.sleep(3)
            player.run = False
            pygame.mouse.set_visible(True)

        if player.get_level() == 10 and boss_entry:
            redraw_window()
            time.sleep(2)
            boss_entry = False
        elif player.get_level() > 10:
            win = True
            redraw_window()
            time.sleep(3)
            player.run = False

        if len(enemies + heals) == 0:
            player.set_level()
            wave_length += 4
            wave_length_obs += 3
            wave_length_heal += 1

            for i in range(wave_length if player.get_level() < 10 else 1):
                enemies.append(Enemy(
                    random.randrange(50, config.WIDTH - 100),
                    random.randrange(-1200, -100),
                    random.choice(['easy', 'medium', 'hard']) if player.get_level() < 10 else 'boss')
                )

            for i in range(wave_length_obs if player.get_level() < 10 else 1):
                enemies.append(Obstacle(
                    random.randrange(50, config.WIDTH - 100),
                    random.randrange(-1200, -100),
                    random.choice(['easyObs', 'mediumObs']) if player.get_level() < 10 else 'hardObs')
                )

            # for i in range(wave_length_heal if player.get_level() < 10 else 2):
            #     heals.append(Repair(
            #         random.randrange(50, config.WIDTH - 100),
            #         random.randrange(-1200, -100),
            #         random.choice(['easyHeal']) if player.get_level() < 10 else 'easyHeal')
            #     )

        # if len(obstacles) == 0:
        #     player.set_level()
        #     wave_len += 3

        #     for i in range(wave_len if player.get_level() < 10 else 1):
        #         obstacles.append(Obstacle(
        #             random.randrange(50),
        #             random.randrange(-1200, -100),
        #             random.choice(['easyObs', 'mediumObs', 'hardObs']) if player.get_level() < 10 else 'hardObs'
        #         ))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.VIDEORESIZE:
                if not display_cfg.fullscreen:
                    config.update(event.w, event.h)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pause_btn.isOver():
                        pygame.mouse.set_visible(True)
                        pause = True
                        redraw_window()
                        paused(player, isMouse)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    audio_cfg.toggle_mute()
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    audio_cfg.inc_volume(5)
                if event.key == pygame.K_MINUS:
                    audio_cfg.dec_volume(5)
                if event.key == pygame.K_f:
                    config.update(
                        config.monitor_size[0], config.monitor_size[1])
                    display_cfg.toggle_full_screen()
                if event.key == pygame.K_p:
                    pygame.mouse.set_visible(True)
                    pause = True
                    redraw_window()
                    paused(player, isMouse)

        player.move()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * config.FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.SCORE += 50
                player.KILLS += 1
                if enemy.ship_type == 'boss':
                    if enemy.boss_max_health - 5 <= 0:
                        # note: this is not seen as game is paused as soon as boss health reaches zero
                        # should be fixed in future with a short delay in pausing
                        boss_crash = Explosion(player.x, player.y, size=100)
                        explosion_group.add(boss_crash)

                        enemies.remove(enemy)
                        enemy.boss_max_health = 100
                        player.health -= 100
                    else:
                        enemy.boss_max_health -= 5
                        player.health -= 100
                        # player death explosion
                        crash = Explosion(player.x, player.y)
                        explosion_group.add(crash)
                else:
                    player.health -= 10
                    crash = Explosion(enemy.x, enemy.y)
                    explosion_group.add(crash)
                    enemies.remove(enemy)
            elif enemy.y + enemy.get_height()/2 > config.HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

        # Obstacle
        for obstacle in obstacles[:]:
            obstacle.move(obs_vel)
            # obstacle.move_lasers(laser_vel, player)

            # if random.randrange(0, 2 * config.FPS) == 1:
            #     enemy.shoot()

            if collide(obstacle, player):
                player.SCORE += 25
                player.KILLS += 1

                player.health -= 10
                crash = Explosion(enemy.x, enemy.y)
                explosion_group.add(crash)
                enemies.remove(enemy)

                # if enemy.ship_type == 'boss':
                #     if enemy.boss_max_health - 5 <= 0:
                #         # note: this is not seen as game is paused as soon as boss health reaches zero
                #         # should be fixed in future with a short delay in pausing
                #         boss_crash = Explosion(player.x, player.y, size=100)
                #         explosion_group.add(boss_crash)

                #         enemies.remove(enemy)
                #         enemy.boss_max_health = 100
                #         player.health -= 100
                #     else:
                #         enemy.boss_max_health -= 5
                #         player.health -= 100
                #         # player death explosion
                #         crash = Explosion(player.x, player.y)
                #         explosion_group.add(crash)
                # else:
                #     player.health -= 10
                #     crash = Explosion(enemy.x, enemy.y)
                #     explosion_group.add(crash)
                #     enemies.remove(enemy)
            elif obstacle.y + obstacle.get_height()/2 > config.HEIGHT:
                lives -= 1
                enemies.remove(obstacle)

        player.move_lasers(-laser_vel, obstacles)

        # # Heal
        # for heal in heals[:]:
        #     heal.move(heal_vel)
        #     # obstacle.move_lasers(laser_vel, player)

        #     # if random.randrange(0, 2 * config.FPS) == 1:
        #     #     enemy.shoot()

        #     if collide(heals, player):
        #         # player.SCORE += 25
        #         # player.KILLS += 1

        #         player.health += 10
        #         # crash = Explosion(heal.x, heal.y)
        #         # explosion_group.add(crash)
        #         heals.remove(heal)

        #         # if enemy.ship_type == 'boss':
        #         #     if enemy.boss_max_health - 5 <= 0:
        #         #         # note: this is not seen as game is paused as soon as boss health reaches zero
        #         #         # should be fixed in future with a short delay in pausing
        #         #         boss_crash = Explosion(player.x, player.y, size=100)
        #         #         explosion_group.add(boss_crash)

        #         #         enemies.remove(enemy)
        #         #         enemy.boss_max_health = 100
        #         #         player.health -= 100
        #         #     else:
        #         #         enemy.boss_max_health -= 5
        #         #         player.health -= 100
        #         #         # player death explosion
        #         #         crash = Explosion(player.x, player.y)
        #         #         explosion_group.add(crash)
        #         # else:
        #         #     player.health -= 10
        #         #     crash = Explosion(enemy.x, enemy.y)
        #         #     explosion_group.add(crash)
        #         #     enemies.remove(enemy)
        #     elif heal.y + heal.get_height()/2 > config.HEIGHT:
        #         lives += 1
        #         heals.remove(heal)

        # player.move_lasers(-laser_vel, heals)

def game2(isMouse=False):
    global pause
    lives = 5
    laser_vel = 10

    sub_font = pygame.font.Font(Font.neue_font, 40)
    sub_small_font = pygame.font.Font(Font.neue_font, 35)
    pop_up_font = pygame.font.Font(Font.edit_undo_font, 55)

    # load and play ingame music
    audio_cfg.play_music(Path.GAME_MUSIC_PATH)

    enemies = []
    wave_length = 0
    enemy_vel = 1

    # obstacle
    obstacles = []
    wave_len_obs = 0
    obs_vel = 1

    # obstacle
    heals = []
    wave_len_heal = 0
    heal_vel = 1

    player2 = Player2(config.center_x, 585, mouse_movement=isMouse)
    if isMouse == True:
        pygame.mouse.set_visible(False)
    elif isMouse == False:
        pygame.mouse.set_visible(True)

    lost = False
    win = False
    boss_entry = True

    pause_btn = IconButton(Image.PAUSE_IMAGE)

    explosion_group.empty()

    def redraw_window():
        bg_obj.update()
        bg_obj.render()

        player2.draw()

        for enemyShip in enemies:
            enemyShip.draw()

        if pause == True:
            play_btn.draw((config.center_x, 45), True, True)
        else:
            pause_btn.draw((config.center_x, 45), True, True)

        # Lives
        for index in range(1, lives + 1):
            Assets.image.draw(Image.HEART_IMAGE,
                              (config.starting_x + 37 * index - 7, 30))

        # Draw Text
        Assets.text.draw(f'{player2.get_level()} / 10', sub_small_font, Colors.CYAN,
                         (config.starting_x + 33, 75))

        score = player2.get_score()
        leftScoreIdx = 0
        if score >= 100 and score < 1000:
            leftScoreIdx = 1
        elif score >= 1000:
            leftScoreIdx = 2

        score_label = Assets.text.render(
            f'{score}', sub_font, Colors.GREEN)
        Assets.text.drawSurface(
            score_label, (config.ending_x - score_label.get_width() - 30, 20))
        Assets.image.draw(Image.STAR_IMAGE,
                          (config.ending_x - Image.SKULL_IMAGE.get_width() - 85 - leftScoreIdx*23, 26))

        kills = player2.get_kills()
        leftKillsIdx = 0
        if kills >= 100:
            leftKillsIdx = 1

        Assets.image.draw(Image.SKULL_IMAGE,
                          (config.ending_x - Image.SKULL_IMAGE.get_width() - 85 - leftKillsIdx*15, 82))
        kills_label = Assets.text.render(
            f'{kills}', sub_font, Colors.RED)
        Assets.text.drawSurface(
            kills_label, (config.ending_x - kills_label.get_width() - 30, 75))

        if win:
            scores.append(True, player2.get_level(), player2.get_score(), player2.get_kills())
            Assets.text.draw('WINNER :)', pop_up_font, Colors.GREEN,
                             (config.center_x, 350), True)

        if lost:
            scores.append(False, player2.get_level(), player2.get_score(), player2.get_kills())
            Assets.text.draw('GAME OVER :(', pop_up_font, Colors.RED,
                             (config.center_x, 350), True)

        if player2.get_level() >= 10 and boss_entry:
            Assets.text.draw('BOSS LEVEL!!', pop_up_font, Colors.RED,
                             (config.center_x, 350), True)

        # explosion group
        explosion_group.draw(config.CANVAS)
        explosion_group.update()

        audio_cfg.display_volume()
        pygame.display.flip()
        config.clock.tick(config.FPS)

    while player2.run:
        redraw_window()
        if lives > 0:
            if player2.health <= 0:
                lives -= 1
                player2.health = 100
        else:
            lost = True
            redraw_window()
            time.sleep(3)
            player2.run = False
            pygame.mouse.set_visible(True)

        if player2.get_level() == 10 and boss_entry:
            redraw_window()
            time.sleep(2)
            boss_entry = False
        elif player2.get_level() > 10:
            win = True
            redraw_window()
            time.sleep(3)
            player2.run = False

        if len(enemies) == 0:
            player2.set_level()
            wave_length += 5
            wave_len_heal += 1
            wave_len_obs += 3

            for i in range(wave_length if player2.get_level() < 10 else 1):
                enemies.append(Enemy(
                    random.randrange(50, config.WIDTH - 100),
                    random.randrange(-1200, -100),
                    random.choice(['easy', 'medium', 'hard']) if player2.get_level() < 10 else 'boss')
                )

            for i in range(wave_len_obs if player2.get_level() < 10 else 1):
                enemies.append(Obstacle(
                    random.randrange(50, config.WIDTH - 100),
                    random.randrange(-1200, -100),
                    random.choice(['easyObs', 'mediumObs']) if player2.get_level() < 10 else 'hardObs')
                )

            # for i in range(wave_len_heal if player2.get_level() < 10 else 2):
            #     enemies.append(Repair(
            #         random.randrange(50, config.WIDTH - 100),
            #         random.randrange(-1200, -100),
            #         random.choice(['easyHeal']) if player2.get_level() < 10 else 'easyHeal')
            #     )

        # if len(obstacles) == 0:
        #     player.set_level()
        #     wave_len += 3

        #     for i in range(wave_len if player.get_level() < 10 else 1):
        #         obstacles.append(Obstacle(
        #             random.randrange(50),
        #             random.randrange(-1200, -100),
        #             random.choice(['easyObs', 'mediumObs', 'hardObs']) if player.get_level() < 10 else 'hardObs'
        #         ))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.VIDEORESIZE:
                if not display_cfg.fullscreen:
                    config.update(event.w, event.h)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pause_btn.isOver():
                        pygame.mouse.set_visible(True)
                        pause = True
                        redraw_window()
                        paused(player2, isMouse)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    audio_cfg.toggle_mute()
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    audio_cfg.inc_volume(5)
                if event.key == pygame.K_MINUS:
                    audio_cfg.dec_volume(5)
                if event.key == pygame.K_f:
                    config.update(
                        config.monitor_size[0], config.monitor_size[1])
                    display_cfg.toggle_full_screen()
                if event.key == pygame.K_p:
                    pygame.mouse.set_visible(True)
                    pause = True
                    redraw_window()
                    paused(player2, isMouse)

        player2.move()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player2)

            if random.randrange(0, 2 * config.FPS) == 1:
                enemy.shoot()

            if collide(enemy, player2):
                player2.SCORE += 50
                player2.KILLS += 1
                if enemy.ship_type == 'boss':
                    if enemy.boss_max_health - 5 <= 0:
                        # note: this is not seen as game is paused as soon as boss health reaches zero
                        # should be fixed in future with a short delay in pausing
                        boss_crash = Explosion(player2.x, player2.y, size=100)
                        explosion_group.add(boss_crash)

                        enemies.remove(enemy)
                        enemy.boss_max_health = 100
                        player2.health -= 100
                    else:
                        enemy.boss_max_health -= 5
                        player2.health -= 100
                        # player death explosion
                        crash = Explosion(player2.x, player2.y)
                        explosion_group.add(crash)
                else:
                    player2.health -= 10
                    crash = Explosion(enemy.x, enemy.y)
                    explosion_group.add(crash)
                    enemies.remove(enemy)
            elif enemy.y + enemy.get_height()/2 > config.HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player2.move_lasers(-laser_vel, enemies)

        # Obstacle
        for obstacle in obstacles[:]:
            obstacle.move(obs_vel)
            # obstacle.move_lasers(laser_vel, player)

            # if random.randrange(0, 2 * config.FPS) == 1:
            #     enemy.shoot()

            if collide(obstacle, player2):
                player2.SCORE += 25
                player2.KILLS += 1

                player2.health -= 10
                crash = Explosion(enemy.x, enemy.y)
                explosion_group.add(crash)
                enemies.remove(enemy)

                # if enemy.ship_type == 'boss':
                #     if enemy.boss_max_health - 5 <= 0:
                #         # note: this is not seen as game is paused as soon as boss health reaches zero
                #         # should be fixed in future with a short delay in pausing
                #         boss_crash = Explosion(player.x, player.y, size=100)
                #         explosion_group.add(boss_crash)

                #         enemies.remove(enemy)
                #         enemy.boss_max_health = 100
                #         player.health -= 100
                #     else:
                #         enemy.boss_max_health -= 5
                #         player.health -= 100
                #         # player death explosion
                #         crash = Explosion(player.x, player.y)
                #         explosion_group.add(crash)
                # else:
                #     player.health -= 10
                #     crash = Explosion(enemy.x, enemy.y)
                #     explosion_group.add(crash)
                #     enemies.remove(enemy)
            elif obstacle.y + obstacle.get_height()/2 > config.HEIGHT:
                lives -= 1
                enemies.remove(obstacle)

        player2.move_lasers(-laser_vel, obstacles)

        # # Heal
        # for heal in heals[:]:
        #     heal.move(heal_vel)
        #     # obstacle.move_lasers(laser_vel, player)

        #     # if random.randrange(0, 2 * config.FPS) == 1:
        #     #     enemy.shoot()

        #     if collide(heals, player2):
        #         # player.SCORE += 25
        #         # player.KILLS += 1

        #         player2.health += 10
        #         crash = Explosion(enemy.x, enemy.y)
        #         explosion_group.add(crash)
        #         enemies.remove(enemy)

        #         # if enemy.ship_type == 'boss':
        #         #     if enemy.boss_max_health - 5 <= 0:
        #         #         # note: this is not seen as game is paused as soon as boss health reaches zero
        #         #         # should be fixed in future with a short delay in pausing
        #         #         boss_crash = Explosion(player.x, player.y, size=100)
        #         #         explosion_group.add(boss_crash)

        #         #         enemies.remove(enemy)
        #         #         enemy.boss_max_health = 100
        #         #         player.health -= 100
        #         #     else:
        #         #         enemy.boss_max_health -= 5
        #         #         player.health -= 100
        #         #         # player death explosion
        #         #         crash = Explosion(player.x, player.y)
        #         #         explosion_group.add(crash)
        #         # else:
        #         #     player.health -= 10
        #         #     crash = Explosion(enemy.x, enemy.y)
        #         #     explosion_group.add(crash)
        #         #     enemies.remove(enemy)
        #     elif heal.y + heal.get_height()/2 > config.HEIGHT:
        #         lives += 1
        #         enemies.remove(heal)

        # player2.move_lasers(-laser_vel, heals)


def paused(player, isMouse):
    main_font = pygame.font.Font(Font.edit_undo_font, 60)

    pause_label = Assets.text.render('Paused', main_font, Colors.CYAN)
    Assets.text.drawSurface(
        pause_label, (config.center_x - pause_label.get_width()//2, 300))

    play_2_btn = IconButton(Image.PLAY_IMAGE_2)
    home_btn = IconButton(Image.HOME_IMAGE)

    while pause:
        home_btn.draw((config.center_x+66, 400), True, True)
        play_2_btn.draw((config.center_x-84, 400), True, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_btn.isOver():
                        if isMouse == True:
                            pygame.mouse.set_visible(False)
                        elif isMouse == False:
                            pygame.mouse.set_visible(True)
                        unpause()
                    if play_2_btn.isOver():
                        if isMouse == True:
                            pygame.mouse.set_visible(False)
                        elif isMouse == False:
                            pygame.mouse.set_visible(True)
                        unpause()
                    if home_btn.isOver():
                        scores.append(False, player.get_level(), player.get_score(), player.get_kills())
                        player.run = False
                        unpause()
                        audio_cfg.play_music(Path.MENU_MUSIC_PATH)
                        from main import main
                        main()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if isMouse == True:
                        pygame.mouse.set_visible(False)
                    elif isMouse == False:
                        pygame.mouse.set_visible(True)
                    unpause()
                if event.key == pygame.K_BACKSPACE:
                    scores.append(False, player.get_level(), player.get_score(), player.get_kills())
                    player.run = False
                    unpause()
                    audio_cfg.play_music(Path.MENU_MUSIC_PATH)

        pygame.display.flip()
        config.clock.tick(15)


def unpause():
    global pause
    pause = False
    # audio_cfg.play_music(Path.PROLOGUE_MUSIC_PATH)
    # from main import main
    # main()
