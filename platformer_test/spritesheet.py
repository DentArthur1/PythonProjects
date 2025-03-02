
import pygame



class Spritesheet():

    def __init__(self):

        self.spritesheet = pygame.image.load("player_sprites/spritesheet.png")
        self.img_width, self.img_height = 24,24

    def get_image(self,index):

        img_surface = pygame.surface.Surface((self.img_width, self.img_height))
        img_surface.set_colorkey((0,0,0))
        img_surface.blit(self.spritesheet,(0,0), ((index * self.img_width) ,0,self.img_width, self.img_height))
        return img_surface