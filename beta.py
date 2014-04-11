import time
import random
from random import randint
import sys, pygame
from pygame.locals import*
pygame.init()
icon=pygame.image.load("enemy.png")
title='Dodge Game (Press Q to return to Home Screen)'

class interact:#this class takes care of the player movements, collision between platforms, jump, and etc

    def __init__(self,x,y,collide,land,jumpcounter,jump,changeX1,changeX2,changeY1,changeY2,alive): #declear all calss variables needed
        self.x=x;self.y=y
        self.collide=collide
        self.land=land;self.jump=jump;self.jumpcounter=jumpcounter
        self.changeX1=changeX1;self.changeX2=changeX2;self.changeY1=changeY1;self.changeY2=changeY2
        self.alive=alive

    def display(self,item,screen):#display function
        screen.blit(item,(self.x,self.y))

    def update(self,plat):#collision between player and platforms
        self.x+=(self.changeX1+self.changeX2)
        if self.x<0 or self.x>620: self.x-=(self.changeX1+self.changeX2)
        for stuff in plat:#go through all the platform x,y if they overlap or not
            if (stuff.x-20)<self.x<(stuff.x+100) and (stuff.y-20)<self.y<(stuff.y+25):self.x-=(self.changeX1+self.changeX2)
        self.y+=(self.changeY1+self.changeY2)
        if self.y<0: self.y-=(self.changeY1+self.changeY2);self.collide=1#collide variable to indicate jump should be over when collided with platforms
        for stuff in plat:
            if (stuff.x-20)<self.x<(stuff.x+100) and (stuff.y-20)<self.y<(stuff.y+25):#if they do overlap the coordinate would simply become the platform's border
                if (stuff.y-22)<self.y<(stuff.y+10):self.y=stuff.y-20
                elif (stuff.y+10)<self.y<(stuff.y+25):self.y=stuff.y+25;self.collide=1
        for stuff in plat:
            if (stuff.x-20)<self.x<(stuff.x+100) and self.y==(stuff.y-20):self.land=1;break#land variable to reset jump so you can jump again
            else:self.land=0
        if self.y>480:self.alive=0#if they fall under the screen they are dead

    def revivefn(self,otherplayer):#used in multiplayer to revive another player when by touching
        if self.alive==0:
            if (otherplayer.x-20)<self.x<(otherplayer.x+20) and (otherplayer.y-20)<self.y<(otherplayer.y+20):#revive if they touch eachother
                    self.alive=1

    def jumpfn(self):#jump function
        if self.jump==1:
            if self.collide==1:self.changeY1=0;self.jumpcounter=0;self.jump=0;self.collide=0#once the player hit something jump is over
            elif 0<=self.jumpcounter<10:self.jumpcounter+=1#various counters to put y coordinate changes to make the jump smoother
            elif 10<=self.jumpcounter<17:self.changeY1=-6;self.jumpcounter+=1
            elif 17<=self.jumpcounter<22:self.changeY1=-5;self.jumpcounter+=1
            elif 22<=self.jumpcounter<25:self.changeY1=-4;self.jumpcounter+=1
            elif 25<=self.jumpcounter<28:self.changeY1=-3;self.jumpcounter+=1
            elif 28<=self.jumpcounter<33:self.changeY1=-1;self.jumpcounter+=1
            else:self.changeY1=0;self.jumpcounter=0;self.jump=0

class platforms:#class simply for displaying the platforms

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def display(self,item,screen):
        screen.blit(item,(self.x,self.y))

class enemystuff:#class for enemy, the red circles movements and interactions with the player

    def __init__(self,x,y,repeatx,repeaty):
        self.x=x
        self.y=y
        self.repeatx=repeatx
        self.repeaty=repeaty

    def display(self,item,screen):
        screen.blit(item,(self.x,self.y))

    def enemyupdate(self,player,player2,enemyspeed):#set up the movements such that when it hits the border it bounces 45 degree off
        if self.x<0 or self.x>620:self.repeatx=self.repeatx*-1
        if self.y<0 or self.y>460:self.repeaty=self.repeaty*-1
        if self.repeatx==1:self.x+=enemyspeed
        elif self.repeatx==-1:self.x-=enemyspeed#with a changeable speed
        if self.repeaty==1:self.y+=enemyspeed
        elif self.repeaty==-1:self.y-=enemyspeed
        if player.alive==1:#if it hits an alive player it will kill it
            if (self.x-20)<player.x<(self.x+20) and (self.y-20)<player.y<(self.y+20):player.alive=0
        if player2.alive==1:
            if (self.x-20)<player2.x<(self.x+20) and (self.y-20)<player2.y<(self.y+20):player2.alive=0

def introscreen():#the intro screen to select modes
    pygame.display.set_icon(icon)#a title and icon for the window
    pygame.display.set_caption(title)
    size=width, height=640, 480
    font=pygame.font.SysFont("Arial",16)
    instructionlbl=font.render("<Controls>  [1 Player] Left,Right,Space  [2 Player] A,D,W & Left,Right,Up", 1, (255,255,255))
    black=0,0,0
    screen=pygame.display.set_mode(size)
    frame=pygame.time.Clock()
    intro,redball,xcounter,ycounter,x,y = pygame.image.load("intro.png"),pygame.image.load("enemy.png"),1,1,0,0

    while(1):
        mousex,mousey = pygame.mouse.get_pos()#check player's selection based on the position of their mouse click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:pygame.quit();sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if 169<mousex<464 and 175<mousey<285:main(1)#game mode is been carried through as an arguement
            if event.type == MOUSEBUTTONDOWN:
                if 169<mousex<464 and 300<mousey<408:main(2)
        if x<0 or x>620:xcounter=xcounter*-1#movement for the red dot
        if y<0 or y>460:ycounter=ycounter*-1#counter to achieve the bounce off effect
        if xcounter==1:x+=2
        elif xcounter==-1:x-=2
        if ycounter==1:y+=2
        elif ycounter==-1:y-=2
        screen.fill(black)
        screen.blit(intro,(0,0))
        screen.blit(redball,(x,y))
        screen.blit(instructionlbl,(80,440))#display the control instructions
        pygame.display.flip()
        frame.tick(60)

def main(mode):
    pygame.display.set_icon(icon)
    pygame.display.set_caption(title)#a title and icon for the window
    size=width, height=640, 480
    font=pygame.font.SysFont("Times New Roman",20)
    black=0,0,0
    platcounter,timemark,enemyspeed=0,pygame.time.get_ticks(),1#initialize all the variables
    screen=pygame.display.set_mode(size)
    frame=pygame.time.Clock()
    gamestart=(pygame.time.get_ticks())#keep track when the game started to further calculate score
    greendot=[pygame.image.load("greendot.png"),pygame.image.load("greendot_dead.png")]#load the images used in the game
    bluesqr =[pygame.image.load("bluesquare.png"),pygame.image.load("bluesquare_dead.png")]
    enemypic, platform = pygame.image.load("enemy.png"),pygame.image.load("platform0.png")
    if mode==1:p1jumpkey=K_SPACE#key settings for different mode
    elif mode==2:p1jumpkey=K_UP

    if mode==1:player=interact(60,0,0,0,0,0,0,0,0,3,1);player2=interact(-100,-100,0,0,0,0,0,0,0,3,0)#check the mode and initial player(s)
    elif mode==2:player=interact(60,0,0,0,0,0,0,0,0,3,1);player2=interact(120,0,0,0,0,0,0,0,0,3,1)

    enemy=[]#create a list for enemy and platforms
    plat=[platforms(32,67),platforms(265,80),platforms(508,67),platforms(96,133),platforms(432,133),platforms(184,196),platforms(349,195),platforms(35,254),platforms(267,257),platforms(508,256),platforms(186,315),platforms(350,315),platforms(110,379),platforms(425,378),platforms(266,421),platforms(8,442),platforms(534,442)]
    while(1):
        score=pygame.time.get_ticks()-gamestart#keep update the score by using the time
        scorelbl=font.render("Score: "+str(score), 1, (255,255,255))
        if player.alive==0 and player2.alive==0:gameover(gamestart)#check if game is over
        for event in pygame.event.get():#take keyboard inputs
            if event.type == pygame.QUIT:pygame.quit();sys.exit()
            if event.type == KEYDOWN:
                if event.key == p1jumpkey:#when jump key is pressed check if the player is in contact with any platform
                    if player.land==1:player.changeY1=-7;player.jump=1;player.land=0#if it is enable jump and related variables
                if event.key == K_LEFT:
                    player.changeX1=-2
                if event.key == K_RIGHT:
                    player.changeX2=2
                if event.key == K_w:
                    if player2.land==1:player2.changeY1=-7;player2.jump=1;player2.land=0
                if event.key == K_a:
                    player2.changeX1=-2
                if event.key == K_d:
                    player2.changeX2=2
                if event.key == K_q:
                    introscreen()
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    player.changeX1=0
                if event.key == K_RIGHT:
                    player.changeX2=0
                if event.key == K_a:
                    player2.changeX1=0
                if event.key == K_d:
                    player2.changeX2=0
        if len(enemy)<12:#generating new enemy based on time
            if  pygame.time.get_ticks()>=(timemark+2000):
                if randint(1, 4)==1:enemy.append(enemystuff(randint(0, 620),0,1,1))
                elif randint(1, 4)==2:enemy.append(enemystuff(0,randint(0, 460),1,1))
                elif randint(1, 4)==3:enemy.append(enemystuff(620,randint(0, 460),1,1))
                elif randint(1, 4)==4:enemy.append(enemystuff(randint(0, 620),460,1,1))
                timemark=pygame.time.get_ticks()
        else:#speed up the enemy speed once number of enemy reached limit
            if  pygame.time.get_ticks()>=(timemark+15000):
                if enemyspeed<5:enemyspeed+=1;timemark=pygame.time.get_ticks()
                else: pass

        screen.fill(black)
        screen.blit(scorelbl,(260,461))#display the current score

        if player.alive==1:player.jumpfn();player.update(plat)#if player is alive update position and allow to jump
        elif player.alive==0:player.revivefn(player2)#if not run the revive fn to check if other player is in contact to revive
        if player2.alive==1:player2.jumpfn();player2.update(plat)
        elif player2.alive==0:player2.revivefn(player)

        for stuff in enemy:#check if any enemy is in collision with the player
            stuff.enemyupdate(player,player2,enemyspeed)

        for stuff in plat:stuff.display(platform,screen)#display the platforms

        if player.alive==1:player.display(greendot[0],screen)#if the player is alive standard icon is displayed
        elif player.alive==0:player.display(greendot[1],screen)#if not the icon is been displayed as transparent represent the player is dead like a ghost
        if player2.alive==1:player2.display(bluesqr[0],screen)
        elif player2.alive==0:player2.display(bluesqr[1],screen)

        for stuff in enemy:#display all the enemies
            stuff.display(enemypic,screen)

        pygame.display.flip()
        frame.tick(60)

def gameover(startime):#gameover screen with game start time as arguement
    pygame.display.set_icon(icon)#a title and icon for the window
    pygame.display.set_caption(title)
    size=width, height=640, 480
    ggscreen=pygame.image.load("ggscreen.png")
    screen=pygame.display.set_mode(size)
    frame=pygame.time.Clock()
    score=pygame.time.get_ticks()-startime#use the game start time and current time to calculate how long the player(s) survived as score
    font=pygame.font.SysFont("Times New Roman",55)
    scorelbl=font.render("Score: "+str(score), 1, (255,255,255))#display the score

    while(1):
        mousex,mousey = pygame.mouse.get_pos()#check for user mouse click to go back to menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:pygame.quit();sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if 199<mousex<427 and 362<mousey<442:introscreen()
        screen.blit(ggscreen,(0,0))
        screen.blit(scorelbl,(195,200))
        pygame.display.flip()
        frame.tick(60)

introscreen()