import pygame
import sys

from .background import slow_bg_obj
from models.icon_button import IconButton
from models.controls import audio_cfg, display_cfg
from utils.assets import Assets
from config import config
from constants import Image, Font, Colors, Text, Path
from models.button import Button
from screens.game import game, game2


def prologoue():
    ships_title_font = pygame.font.Font(Font.edit_undo_font, 50)
    ships_info_font = pygame.font.Font(Font.neue_font, 22)

    audio_cfg.play_music(Path.PROLOGUE_MUSIC_PATH)

    go_back_btn = IconButton(Image.GO_BACK_IMAGE)
    mouse_btn = Button(Colors.BACKGROUND_BLACK, Colors.WHITE, "MOUSE")
    keyboard_btn = Button(Colors.BACKGROUND_BLACK, Colors.WHITE, "Plane 1")
    keyboard2_btn = Button(Colors.BACKGROUND_BLACK, Colors.WHITE, "Plane 2")

    NEW_HEART_IMAGE = pygame.transform.scale(
        Image.HEART_IMAGE, (Image.HEART_IMAGE.get_width()*3/4, Image.HEART_IMAGE.get_height()*3/4))

    run = True
    while run:
        slow_bg_obj.update()
        slow_bg_obj.render()

        
        # CutScene Pertama
        Assets.image.draw(Image.GOTG, (config.center_x + 0, 80), True)
        Assets.text.draw('"Guardian of the Galaxy: Pilot a fearless spaceship through ', ships_info_font, Colors.WHITE,
                         (config.center_x + -300, 455))
        Assets.text.draw('treacherous galaxies, defending humanity from alien threats."', ships_info_font, Colors.WHITE,
                         (config.center_x + -300, 500))
        

        go_back_btn.draw((config.starting_x + 65, 50), True, True)

        # mouse_btn.draw(
        #     (config.center_x - 210, config.center_y + 42), (195, 66))
        
        keyboard_btn.draw(
            (config.center_x - 210, config.center_y + 192), (185, 60))
        
        keyboard2_btn.draw(
            (config.center_x + 25, config.center_y + 192), (185, 60))
        

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
                        audio_cfg.play_music(Path.MENU_MUSIC_PATH)
                    # if mouse_btn.isOver():
                    #     game(True)
                    if keyboard_btn.isOver():
                        game()
                    if keyboard2_btn.isOver():
                        game2()

            # Mouse hover events
            if event.type == pygame.MOUSEMOTION:
                if go_back_btn.isOver():
                    go_back_btn.outline = True
                else:
                    go_back_btn.outline = False
                    

                # if mouse_btn.isOver():
                #     mouse_btn.outline = True
                # else:
                #     mouse_btn.outline = False

                if keyboard_btn.isOver():
                    keyboard_btn.outline = True
                else:
                    keyboard_btn.outline = False

                if keyboard2_btn.isOver():
                    keyboard2_btn.outline = True
                else:
                    keyboard2_btn.outline = False
