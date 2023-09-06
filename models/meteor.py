import pygame

from utils.assets import Assets
from config import config
from constants import  Image

from config import config
from utils.collide import collide
from utils.assets import Assets


class Meteor:
    def __init__(self, x, y, img, health=100):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.health = health
        self.obs_img = None
        self.dmg_img = None
        self.SCORE = 0
        self.KILLS = 0
        self.level = 0

    def draw(self):
        # making laser's coordinates centered in the sprite
        Assets.image.draw(
            self.img, (config.starting_x + self.x, self.y), True, True)

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(height >= self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

class Obstacle(Meteor):
    TYPE_MODE = {
        'easyObs': (Image.EASY_OBSTACLE, 7),
        'mediumObs': (Image.MEDIUM_OBSTACLE, 12),
        'hardObs': (Image.HARD_OBSTACLE, 20)
    }

    obs_type = ''

    def __init__(self, x, y, obs_type, health=100):
        super().__init__(x, y, health)
        self.obs_type = obs_type
        self.obs_img, self.damage = self.TYPE_MODE[self.obs_type]
        self.mask = pygame.mask.from_surface(self.obs_img)

    def move(self, vel):
        self.y += vel
