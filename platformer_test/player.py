import pygame
class Player():

    def __init__(self):

        self.player_rect = pygame.rect.Rect(0,0,15,17)
        self.vel_y = 5
        self.vel_x = 2
        self.movement = [0,0]
        self.anim_list = [n for n in range(0,21, 1)]
        self.set_point = 200
        self.anim_time = 200
        self.left = False
        self.right = False
        self.moving = False
        self.in_air = True


    def jump(self):
        #if the player is on the ground it lets him jump
        if self.in_air == False:
            self.movement[1] = - self.vel_y
            self.in_air = True

    def add_gravity(self,grav_coeff):
        #adds gravity   
        self.movement[1] += grav_coeff 
        if self.movement[1] >= self.vel_y: #limits the gravity force to 5
            self.movement[1] = self.vel_y
        

    def check_collisions(self, tiles):
        hits = []
        #loops though the tiles anc checks for collisions
        for tile in tiles:
            if tile.colliderect(self.player_rect):
                   hits.append(tile)

        return hits

    def move(self, tiles):
        #checks for collisions and updates player position on one axis before moving to another
        self.player_rect.x += self.movement[0]
        hits = self.check_collisions(tiles)
        for tile in hits:
            if self.movement[0] > 0:
                self.player_rect.right = tile.left
                
              
            elif self.movement[0] < 0:
                self.player_rect.left = tile.right
        #checks if player is moving or not
        if self.movement[0] != 0:
            self.moving = True
        else:
            self.moving = False
        #handles hits by moving the player on the y axis      
        self.player_rect.y += self.movement[1]
        hits = self.check_collisions(tiles)
        for tile in hits:
            if self.movement[1] > 0:
                self.player_rect.bottom = tile.top
                self.in_air = False
                
            elif self.movement[1] < 0:
                self.player_rect.top = tile.bottom
                
            self.movement[1] = 0

    def animate(self, current_time,index): #jumping, standing, walking
        #checks for bools and determines the correct chunk of the list to use
        if self.moving:
            list = self.anim_list[5:9]
            self.anim_time = 100

        elif self.moving == False:
            list = self.anim_list[0:2]
            self.anim_time = 1000

        if self.in_air:
            list = self.anim_list[3:4]
        #for instantly activating the animation
        if self.set_point - current_time > self.anim_time:    
                self.set_point = current_time
         #if the set point has been reached --> do the animation
        if current_time >= self.set_point:
            if list[0] <= index <= list[-1]:  #checks if the animation has been changed or not, if index is in list then it hasn't
                index += 1
                if index > list[-1]: #if the index is > of the index of the last item in the list, it resets the index to the first value of the list
                    index = list[0]
            else:
                index = list[0]    #changing animation

            self.set_point += self.anim_time     #changes sprite every x milliseconds
        return index

    
        
