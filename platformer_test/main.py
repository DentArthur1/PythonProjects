
import pygame
from map import *
from player import *
from spritesheet import *

class Game():

    def __init__(self):

        self.width = 600
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.icon = pygame.image.load("imgs/viking.png")
        self.running = True
        self.FPS = 75
        self.map = Map()
        self.player = Player()
        self.rects =[]
        self.gravity_coeff = 0.1
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Test")

    def blit_map(self, index):
       #give the index to render the correct sprite      goes from 0 to 20 
       upscale, self.rects = self.map.get_upscale(self.map.spritesheet.get_image(index), self.player.player_rect, self.screen,self.player.left)
       self.screen.blit(upscale,(0,0))

    def handle_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_a:
                    self.player.left = True
                    self.player.right = False 
                    self.player.movement[0] =  - self.player.vel_x
                    
                if event.key == pygame.K_d:
                    self.player.right = True
                    self.player.left = False
                    self.player.movement[0] =    self.player.vel_x
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                   self.player.movement[0] = 0
                   
                if event.key == pygame.K_d:
                   self.player.movement[0] = 0
                  
                    
    
    def main_loop(self):
        index = 0
        while self.running:
            self.map.map_surface.fill((0,34,0)) #update the to-be-scaled surface
            self.screen.fill((0,34,0))  #update the main surface
            current_time = pygame.time.get_ticks()
            index = self.player.animate(current_time,index)

            self.blit_map(index) #blits map and player correctly scaled
            self.handle_events()  #handles user inputs


            self.player.add_gravity(self.gravity_coeff) #simulates gravity 
            self.player.move(self.rects)  #checks for collisions and moves the player with the inputs given
            self.map.move_map(self.player.player_rect)
            self.clock.tick(self.FPS) #limits the fps to the value given
            pygame.display.flip()


game = Game()
game.main_loop()