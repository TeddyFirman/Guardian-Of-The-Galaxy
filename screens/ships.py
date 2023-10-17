import pygame
import sys

from .background import slow_bg_obj
from models.icon_button import IconButton
from models.controls import audio_cfg, display_cfg
from utils.assets import Assets
from config import config
from constants import Image, Font, Colors, Text


def ships():
    ships_title_font = pygame.font.Font(Font.edit_undo_font, 50)
    ships_info_font = pygame.font.Font(Font.neue_font, 22)

    go_back_btn = IconButton(Image.GO_BACK_IMAGE)

    NEW_HEART_IMAGE = pygame.transform.scale(
        Image.HEART_IMAGE, (Image.HEART_IMAGE.get_width()*3/4, Image.HEART_IMAGE.get_height()*3/4))

    run = True
    while run:
        slow_bg_obj.update()
        slow_bg_obj.render()

    

        # Name: Easy Spaceship; Health: 100; Damage: 10;
        Assets.image.draw(Image.EASY_SPACE_SHIP,
                          (config.center_x - 270, 110), True)
        Assets.text.draw('Easy Spaceship', ships_info_font, Colors.BLUE,
                         (config.center_x - 210, 95))
        Assets.text.draw('Health: 100', ships_info_font,
                         Colors.GREEN, (config.center_x - 210, 122))
        Assets.text.draw('Damage: 10', ships_info_font,
                         Colors.RED, (config.center_x - 210, 149))

        # Name: Medium Spaceship; Health: 100; Damage: 18;
        Assets.image.draw(Image.MEDIUM_SPACE_SHIP,
                          (config.center_x - 270, 235), True)
        Assets.text.draw('Medium Spaceship', ships_info_font, Colors.BLUE,
                         (config.center_x - 210, 230))
        Assets.text.draw('Health: 100', ships_info_font,
                         Colors.GREEN, (config.center_x - 210, 257))
        Assets.text.draw('Damage: 18', ships_info_font,
                         Colors.RED, (config.center_x - 210, 284))

        # Name: Hard Spaceship; Health: 100; Damage: 25;
        Assets.image.draw(Image.HARD_SPACE_SHIP,
                          (config.center_x - 270, 390), True)
        Assets.text.draw('Hard Spaceship', ships_info_font, Colors.BLUE,
                         (config.center_x - 210, 370))
        Assets.text.draw('Health: 100', ships_info_font,
                         Colors.GREEN, (config.center_x - 210, 397))
        Assets.text.draw('Damage: 25', ships_info_font,
                         Colors.RED, (config.center_x - 210, 424))

        # Name: Your Spaceship; Lives: 5; Health: 100; Damage: 100
        Assets.image.draw(Image.PLAYER_SPACE_SHIP,
                          (config.center_x + 260, 110), True)
        Assets.text.draw('Your Spaceship 1', ships_info_font, Colors.BLUE,
                         (config.center_x + 70, 105))
        for index in range(1, 6):
            Assets.image.draw(
                NEW_HEART_IMAGE, (config.center_x + 45 + 25 * index, 132))
        Assets.text.draw('Health: 100', ships_info_font,
                         Colors.GREEN, (config.center_x + 70, 159))
        Assets.text.draw('Damage: 100', ships_info_font,
                         Colors.RED, (config.center_x + 70, 186))
        

        Assets.image.draw(Image.PLAYER2_SPACE_SHIP,
                          (config.center_x + 260, 300), True)
        Assets.text.draw('Your Spaceship 2', ships_info_font, Colors.BLUE,
                         (config.center_x + 70, 295))
        for index in range(1, 6):
            Assets.image.draw(
                NEW_HEART_IMAGE, (config.center_x + 45 + 25 * index, 322))
        Assets.text.draw('Health: 100', ships_info_font,
                         Colors.GREEN, (config.center_x + 70, 349))
        Assets.text.draw('Damage: 100', ships_info_font,
                         Colors.RED, (config.center_x + 70, 376))
        
        # # Name: Hard Spaceship; Health: 100; Damage: 25;
        # Assets.image.draw(Image.EASY_OBSTACLE,
        #                   (config.center_x - 270, 420), True)
        # Assets.text.draw('Easy Obstacle', ships_info_font, Colors.BLUE,
        #                  (config.center_x - 210, 400))
        # Assets.text.draw('Health: 100', ships_info_font,
        #                  Colors.GREEN, (config.center_x - 210, 427))
        # Assets.text.draw('Damage: 25', ships_info_font,
        #                  Colors.RED, (config.center_x - 210, 454))

        # Name: Boss Spaceship; Health: 1980; Damage: 100;
        Assets.image.draw(Image.BOSS_SHIP, (config.center_x, 450), True)
        Assets.text.draw('Boss Spaceship', ships_info_font, Colors.BLUE,
                         (config.center_x + 150, 505))
        Assets.text.draw('Health: 1980', ships_info_font,
                         Colors.GREEN, (config.center_x + 150, 532))
        Assets.text.draw('Damage: 100', ships_info_font,
                         Colors.RED, (config.center_x + 150, 559))

        go_back_btn.draw((config.starting_x + 65, 50), True, True)

        audio_cfg.display_volume()
        config.clock.tick(config.FPS)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.VIDEORESIZE:
                if not display_cfg.fullscreen:
                    config.update(event.w, event.h)

            if event.type == pygame.KEYUP:
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
                if event.key == pygame.K_BACKSPACE:
                    run = False

            # Mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if go_back_btn.isOver():
                        run = False

            # Mouse hover events
            if event.type == pygame.MOUSEMOTION:
                if go_back_btn.isOver():
                    go_back_btn.outline = True
                else:
                    go_back_btn.outline = False
