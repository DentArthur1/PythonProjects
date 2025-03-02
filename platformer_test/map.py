

import pygame
import csv
from spritesheet import *

class Map():

    def __init__(self):

        self.tile_size = 20
        self.grass_img = pygame.image.load("tiles/grass.png")
        self.dirt_img = pygame.image.load("tiles/dirt.png")
        self.file = "map.csv"
        self.map_size = 300,200
        self.spritesheet = Spritesheet()
        self.movement = [0,0]
        self.map_surface = pygame.surface.Surface((self.map_size[0], self.map_size[1]))
        self.map_surface.set_colorkey((0,0,0,0))

    def load_csv(self, file):
         map = []
         #opens the csv file and, with the help of csv library, it reads and appends all the numbers in list "map"
         with open(file, "r") as f:
            content = csv.reader(f, delimiter = ",")
            for row in content:
                map.append(row)

         return map 

    def get_map(self, file):
        map = self.load_csv(file) 
        x, y = 0,0
        tiles_rects = []
        movement = self.movement.copy()
        movement[0], movement[1] = int(movement[0]), int(movement[1])    #to prevent buggy blitting
        
        #loops through all the values in map and draws them on the surface correspondly
        for row in map:
            x = 0
            for tile in row:
                #if the tile is one it places the grass image in the correct position based on the tile index in the map
                #this tile represents the dirt
                if tile == "1":
                    self.map_surface.blit(self.dirt_img, (x * self.tile_size - movement[0], y * self.tile_size - movement[1]))
              
                elif tile == "0":
                    self.map_surface.blit(self.grass_img, (x * self.tile_size - movement[0], y * self.tile_size - movement[1]))
          
                if tile != "-1":
                    tile_rect = pygame.rect.Rect((x * self.tile_size),(y * self.tile_size),self.tile_size,self.tile_size)
                    tiles_rects.append(tile_rect) 
                x += 1
            y += 1

        return self.map_surface, tiles_rects

        
    def get_upscale(self, player_img, rect, screen, left):
        
        map,rects = self.get_map(self.file)
        if left: #flips the image and corrects the img coords
             rot_img = pygame.transform.flip(player_img, True, False)
             map.blit(rot_img,(rect.x - self.movement[0] -8, rect.y - self.movement[1] ))  #-8 is the correction for the spritesheet
        else: #blitting the player onto the surface to-be-scaled
             map.blit(player_img,(rect.x - self.movement[0] , rect.y - self.movement[1] )) 
        upscale = pygame.transform.scale(map, (screen.get_width(), screen.get_height())) #scaling the surface and giving it to the main file

        return upscale, rects

    def move_map(self, rect):
        #i subtract the value of the player to the value of the movement of the map, and ultimately i subtract half the size of the to_be_scaled display, to make the player appear in the center
        self.movement[0] += (rect.x - self.movement[0] - (self.map_size[0] / 2) + 10) / 20       #/20 is used just for making a lerp effect on the camera
        self.movement[1] += (rect.y - self.movement[1] - (self.map_size[1] / 2) + 10) / 20

