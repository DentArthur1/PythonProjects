from random import randrange

import pygame


screen=pygame.display.set_mode((500,400))
icon=pygame.image.load("pong.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Pong")

# player rectangle
player_rect=pygame.rect.Rect(10,10,14,65)
player_rect_x=45
player_rect_y=100
player_recty_change=0

#ai rectangle
ai_rect=pygame.rect.Rect(10,10,14,65)
ai_rect_x=455
ai_rect_y=100
ai_recty_change=0.06

#Ball
ball_rect=pygame.rect.Rect(10,10,14,14)
ball_x=300
ball_y=200
ballx_change=-0.05
bally_change=0.01

#pause
pygame.font.init()
font=pygame.font.Font(None,60)
resume=font.render("Resume",True,(250, 250, 250))
resume_rect=resume.get_rect()
resume_rect.center=255,160
to_menu=font.render("Menu",True,(250, 250, 250))
to_menu_rect=to_menu.get_rect()
to_menu_rect.center=235,207
menu_prin=font.render("Play",True,(250, 250, 250))
menu_prin_rect=menu_prin.get_rect()
menu_prin_rect.center=250,184

# sound effect
pygame.mixer.init()
bar_sound=pygame.mixer.Sound("bar.wav")
wall_sound=pygame.mixer.Sound("wall.wav")
win_sound=pygame.mixer.Sound("win.wav")
bar_sound.set_volume(0.3)
wall_sound.set_volume(0.3)
win_sound.set_volume(0.3)
#winning
win=font.render("win",True,(250,250,250))

#-------------------------------------------------------------------------------------------------
class Rectangles:

    def blit_player_rect(self,x,y):
        player_rect.center=x,y
        pygame.draw.rect(screen,color="white",rect=player_rect)

    def blit_ai_rect(self,x,y):
        ai_rect.center=x,y
        pygame.draw.rect(screen,color="white",rect=ai_rect)



class Ball:
    def blit_ball(self,x,y):
        ball_rect.center=x,y
        pygame.draw.rect(screen,color="white",rect=ball_rect)

    def respwan_ball(self):
        ball_x=230
        ball_y=randrange(20,400,20)
        return ball_x,ball_y


    def ball_to_player(self,baller,count,choice):
        
        if choice[0]==True:
            ballx_change=-0.03
           
        elif choice[1]==True:
            ballx_change=0.03
            

        if baller>0:
            bally_change=-0.02
        else:
            bally_change=0.02
        count+=1
        choice[0]=not choice[0]
        choice[1]=not choice[1]
        return ballx_change,bally_change,count,choice
        



class Settings:
   
  

    def pause_game(self):
        pause=True
        font_change_color=(250,250,250)
        font_change_color2=(250,250,250)
        while pause:
            screen.fill((0,0,0))
            resume=font.render("Resume",True,font_change_color)
            to_menu=font.render("Menu",True,font_change_color2)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.display.quit()
                    
                if event.type==pygame.KEYDOWN:

                    if event.key==pygame.K_ESCAPE:
                        pause=False 

                if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                   if resume_rect.collidepoint(pygame.mouse.get_pos()):
                       pause=False
                   if to_menu_rect.collidepoint(pygame.mouse.get_pos()):
                       pause=False
                       n=1
                       settings.menu()
                       return n

            if resume_rect.collidepoint(pygame.mouse.get_pos()):
                font_change_color=(100,100,100)
            else:
                font_change_color=(250,250,250)
            
            if to_menu_rect.collidepoint(pygame.mouse.get_pos()):
                font_change_color2=(100,100,100)
            else:
                font_change_color2=(250,250,250)

           
            screen.blit(resume,(175,140))
            screen.blit(to_menu,(175,190))
            pygame.display.update()

    def menu(self):
        menus=True
        font_change_color=(250,250,250)
        while menus:
            screen.fill((0,0,0))
            menu=font.render("Play",True,font_change_color)
            for event in pygame.event.get():

                if event.type==pygame.QUIT:
                     pygame.display.quit()
                
                if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    if menu_prin_rect.collidepoint(pygame.mouse.get_pos()):
                        menus=False
                        n=1
                        return n  #devo imparare a usare le funzioni init
                       
                        
            if menu_prin_rect.collidepoint(pygame.mouse.get_pos()):
                font_change_color=(100,100,100)
            else:
                font_change_color=(250,250,250)


            
            screen.blit(menu,(207,164))
            pygame.display.update()
        

    def reset(self):
        count_1,count_2=0,0
        player_rect_x,player_rect_y=45,100
        ai_rect_x,ai_rect_y=455,100
        ball_x,ball_y=230,200
        return count_1,count_2,player_rect_x,player_rect_y,ai_rect_x,ai_rect_y,ball_x,ball_y

#---------------------------------------------------------------------------------------------------------------

rectangles=Rectangles()
ball=Ball()
settings=Settings()

n=0
count_1=0
count_2=0
times=0
move=True

respawn_counter=False
pause=False
running=True
choice=[False,True]

settings.menu()
while running:
    screen.fill((0,0,0)) 
    count=font.render(f"{count_1}  |  {count_2}",True,(250, 250, 250))
    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w:
                player_recty_change=-0.09
            if event.key==pygame.K_s:
                player_recty_change=0.09
            if event.key==pygame.K_ESCAPE:
                n=settings.pause_game()
                if n==1:
                    count_1,count_2,player_rect_x,player_rect_y,ai_rect_x,ai_rect_y,ball_x,ball_y=settings.reset()   
                    n=0  
       
        if event.type==pygame.KEYUP:
            player_recty_change=0

    #limiti player bordo mappa
    if player_rect_y<=30:
        player_rect_y=30
    if player_rect_y>=370:
        player_rect_y=370    

   



    #collisione palla con i rect e rimbalzo proporzionale---------------------------------
    if player_rect.colliderect(ball_rect) and times!=0:
        bar_sound.play()
        player_rate=ball_y-player_rect_y
        ballx_change=0.095
        
        if player_rate>0:  
            bally_change=float(0.002*(player_rate))
        elif player_rate<0: 
            bally_change=float(-0.002*abs(player_rate))
    
    if ai_rect.colliderect(ball_rect) and times!=0:
        bar_sound.play()
        ai_rate=ball_y-ai_rect_y      
        ballx_change=-0.095       
        if ai_rate>0:   
            bally_change=float(0.002*(ai_rate))
        elif ai_rate<0: 
            bally_change=float(-0.002*abs(ai_rate))
    #------------------------------------------------------------------------

    #respawn palla-----------------------------------------------
    if ball_x>=540: 
        win_sound.play()           
        ball_x,ball_y=ball.respwan_ball() 
        baller=ball_y-ai_rect_y    
        ballx_change,bally_change,count_1,choice=ball.ball_to_player(baller,count_1,choice)
       

    if ball_x<=5:       
        win_sound.play()  
        ball_x,ball_y=ball.respwan_ball()  
        baller=ball_y-player_rect_y          
        ballx_change,bally_change,count_2,choice=ball.ball_to_player(baller,count_2,choice)
       
    #-------------------------------------------------------------------    


    #limiti palla soffitto e rimbalzo
    if ball_y<=8:
        wall_sound.play()
        bally_change=+0.05
    if ball_y>=395:
        wall_sound.play()
        bally_change=-0.05

  
    #accelerazione ai 
    if 30<ball_y<370:
       ai_vel_molt=ball_y-ai_rect_y
       if ai_vel_molt>0:
           ai_recty_change=float(0.0015*(ai_vel_molt))
       if ai_vel_molt<=0:
           ai_recty_change=float(-0.0015*abs(ai_vel_molt))

    #limiti ai bordo mappa       
    if ai_rect_y<=30:
       ai_rect_y=30
    if ai_rect_y>=370:
        ai_rect_y=370   

    ai_rect_y+=ai_recty_change 
    player_rect_y+=player_recty_change
    ball_x+=ballx_change
    ball_y+=bally_change
    rectangles.blit_ai_rect(ai_rect_x,ai_rect_y)
    rectangles.blit_player_rect(player_rect_x,player_rect_y)
    ball.blit_ball(ball_x,ball_y)
    screen.blit(count,(200,10))

    #check if someone has won
    if count_1==10 or count_2==10:
        count_1,count_2,player_rect_x,player_rect_y,ai_rect_x,ai_rect_y,ball_x,ball_y=settings.reset() 
        
    times+=1
    pygame.display.update()