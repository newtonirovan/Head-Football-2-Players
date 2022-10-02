add_library('minim')

import random
import time
import os
import math

path = os.getcwd()
player = Minim(this)

WIDTH = 1200
HEIGHT = 800
NET_WIDTH = 128
NET_HEIGHT = 200
BALL_RADIUS = 15
PLAYER_RADIUS = 30
GROUND = 675

class Player:
    def __init__(self, x, y, r, g, n):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.n = n
        self.vx = 0
        self.vy = 0
        self.goal = False
        self.img_n_prv = -1
        self.img_n = 0
        self.img_x1 = 0
        self.img_x2 = 100
        self.key_handler = {LEFT: False, RIGHT: False, UP: False, 'Kick': False}
        self.left = True
        self.right = True
        self.up = True
        self.kick = True
        if self.n == 1:
            self.img = loadImage(path + "/images/" + "head1.png")
        elif self.n == 2:
            self.img = loadImage(path + "/images/" + "head2.png")
    def gravity(self):
        if self.y + self.r < self.g:
            if self.vy < 0:
                self.vy = self.vy + 0.24
            elif self.vy > 0:
                self.vy = self.vy + 0.4
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        else:
            self.vy = 0
    """method used to regulate the interaction of two players"""
    def player_player(self, player):
        self.player = player
        dx = (self.x + self.player.x)/2 # midpoints between them to check interaction
        dy = (self.y + self.player.y)/2 # midpoints between them to check interaction
        
        #taking players as circles and calculating the interaction point
        if (dx - self.x)**2 + (dy - self.y)**2 < self.r**2 and self.vy == 0 and self.player.vy == 0:
            if self.x < self.player.x:
                self.x = dx - self.r
                self.player.x = dx + self.r
                if self.vx != 0:
                    self.player.vx = self.vx
                else:
                    self.vx = self.player.vx
                self.kick = False
                self.right = False
                self.player.kick = False
                self.player.left = False
            elif self.x > self.player.x:
                self.x = dx + self.r
                self.player.x = dx - self.r
                if self.vx != 0:
                    self.player.vx = self.vx
                else:
                    self.vx = self.player.vx
                self.kick = False
                self.left = False
                self.player.kick = False
                self.player.right = False
                
        elif (dx - self.x)**2 + (dy - self.y)**2 < self.r**2 and self.vy != 0:
            if dx < self.player.x:
                self.vx = -2 - self.player.vx
                if self.player.vx > 0:
                    self.vx = -2 - self.player.vx
                else:
                    self.vx = -2 + self.player.vx
                if self.vx > 0:
                    self.vx = -self.vx
                self.vy = 1
                self.motion_v = True
                self.motion_h = True
                self.right = False
                self.player.left = False
                self.player.up = False
                self.up = False
                self.key_handler[UP] = False
                self.player.key_handler[UP] = False
                self.key_handler[RIGHT] = False
                self.player.key_handler[LEFT] = False
            elif dx > self.player.x:
                if self.player.vx > 0:
                    self.vx = 2 + self.player.vx
                else:
                    self.vx = 2 - self.player.vx
                if self.vx < 0:
                    self.vx = -self.vx
                self.vy = 1
                self.motion_v = True
                self.motion_h = True
                self.left = False
                self.player.right= False
                self.key_handler[UP] = False
                self.player.key_handler[UP] = False
                self.key_handler[LEFT] = False
                self.player.key_handler[RIGHT] = False
        
                
        if (dx - self.x)**2 + (dy - self.y)**2 <= self.r**2 and self.y + self.r < self.g and self.player.y + self.player.r < self.g:
            if self.x > self.player.x:
                self.left = False
                self.player.right = False
            self.player.vy = 0
            self.player.up = False
            self.up = False
                
        else:
            self.kick = True
            self.left = True
            self.right = True
            self.up = True
            self.player.right = True
            self.player.up = True
            self.player.kick = True
            self.player.left = True
        
        
    def update(self):
        self.gravity()
        
        if self.n == 1:
            self.player_player(game.player2)
        elif self.n == 2:
            self.player_player(game.player1)
                
        if self.key_handler[LEFT] and self.left: #to the left
            self.vx = -2.5
        elif self.key_handler[RIGHT] and self.right: #to the right
            self.vx = 2.5
        else:
            if self.vx > 0 and self.vy != 0:
                self.vx = self.vx - 0.1
            elif self.vx < 0 and self.vy != 0:
                self.vx = self.vx + 0.1
            else:
                self.vx = 0
        if self.key_handler[UP] and self.y + self.r == self.g and self.up: #moving up
            self.vy = -7
        
        #placement change
        self.y = self.y + self.vy
        self.x = self.x + self.vx
        
        #ground
        if self.y + self.r > self.g:
            self.y = self.g - self.r
        
        #boundries
        if self.x - self.r < 0:
            self.x = self.r
        if self.x + self.r > 1200:
            self.x = 1200 - self.r
        
    def display(self):
        self.update()
        #by changing the self.img_n attribute, we show the movement of the foot
        if self.kick == False:
            limit_img = 300
        else:
            limit_img = 600
        if self.key_handler['Kick'] == True:
            if frameCount % 3 == 0:
                self.img_x1 = self.img_x1 + 100
                self.img_x2 = self.img_x2 + 100
                self.img_n_prv = self.img_n
                self.img_n = self.img_n + 1
                if self.img_x1 >= limit_img:
                    self.img_x1 = limit_img - 100
                    self.img_x2 = limit_img
                    self.img_n = self.img_n - 1
        elif self.img_n > 0:
            if frameCount % 3 == 0:
                self.img_x1 = self.img_x1 - 100
                self.img_x2 = self.img_x2 - 100
                self.img_n_prv = self.img_n
                self.img_n = self.img_n - 1
        else:
            self.img_x1 = 0
            self.img_x2 = 100
        
        if self.n == 1:
            image(self.img, self.x - self.r - 20, self.y - self.r, 100, 80, self.img_x1, 0, self.img_x2, 80)
        elif self.n == 2:
            image(self.img, self.x - self.r - 20, self.y - self.r, 100, 80, self.img_x2, 0, self.img_x1, 80)
            
            
            
class Ball:
    def __init__(self, x, y, r, g):
        self.x = 615
        self.y = 50
        self.r = r
        self.g = g
        self.vx = -0.3
        self.vy = 0
        self.motion_v = True
        self.motion_h = False
        self.img_n = 5
        self.img = loadImage(path + "/images/" + "ball" + str(self.img_n) + ".png")
        
        self.leg_kick = player.loadFile(path + "/sounds/leg_kick.mp3")
        self.head_kick = player.loadFile(path + "/sounds/leg_kick.mp3")
        
    def gravity(self):
        #natural deceleration&accelaration(horizantal)
        if self.y + self.r < self.g and self.vy >= 0 and self.motion_v:
            self.vy = self.vy + 0.2
            if self.y + self.r + self.vy >= self.g:
                time.sleep(0.015)
                self.y = self.g - self.r
                if self.vy < 2.5:
                    self.vy = 0
                    self.motion_v = False
                else:
                    self.vy = -self.vy
        elif self.y + self.r <= self.g and self.vy <= 0 and self.motion_v:
            self.vy = self.vy + 0.6
            if self.vy >= 0:
                self.vy = self.vy
        
        #natural deceleration(horizantal)
        if self.vx > 0 and self.y + self.r == self.g and self.motion_h:
            self.vx = self.vx - 1
            if self.vx < 0:
                self.vx = 0
                self.motion_h = False
        elif self.vx < 0 and self.y + self.r == self.g and self.motion_h:
            self.vx = self.vx + 1
            if self.vx > 0:
                self.vx = 0
                self.motion_h = False
                
        # setting max and min values    
        if self.vx > 25:
            self.vx = 25
        elif self.vx < -25:
            self.vx = -25
            
        if self.vy > 25:
            self.vy = 25
        elif self.vy < -25:
            self.vy = -25
        
    #method used to regulate the interaction of the net and the ball
    def net_ball(self):
        if self.x > 0 and self.x < 134 and self.y + self.r <= 490:
            self.g = 485
            if self.vy == 0:
                self.vx = 2
        elif self.x > 1072 and self.x < 1200 and self.y + self.r <= 490:
            self.g = 485
            if self.vy == 0:
                self.vx = -2
        elif self.y + self.r < 674:
            self.g = 675
            self.motion_v = True
            self.motion_h = True
            
    #the player kicks the ball, according to the leg position velocity and interaction point vary
    def player_ball_kick(self, player):
        self.player = player
    
        self.leg_position = self.player.img_n
        self.pleg_position = self.player.img_n_prv
        
        if self.player.n == 2:
            self.vx = -self.vx 
        
        if self.leg_position == 0: #24 * 28
            self.leg_x1 = self.player.x + 6
            self.leg_x2 = self.leg_x1 + 24
            if self.player.n == 2:
                self.leg_x1 = self.player.x -6
                self.leg_x2 = self.leg_x1 - 24
            self.leg_y1 = self.player.y + self.player.r
            self.leg_y2 = self.leg_y1 + 20
            
            if self.leg_position > self.pleg_position:
                if (self.leg_x1 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.vx = -self.vx
                    self.vy = -self.vy
                elif (self.leg_x1 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.vx = -self.vx
                    self.vy = -self.vy
                elif (self.leg_x2 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.vx = -self.vx
                    self.vy = -self.vy
                elif (self.leg_x2 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.vx = -self.vx
                    self.vy = -self.vy
                
        elif self.leg_position == 1: #27 * 20
            self.leg_x1 = self.player.x - 7
            self.leg_x2 = self.leg_x1 + 27
            if self.player.n == 2:
                self.leg_x1 = self.player.x + 7
                self.leg_x2 = self.leg_x1 - 27
            self.leg_y1 = self.player.y + self.player.r
            self.leg_y2 = self.leg_y1 + 20
            
            if self.leg_position > self.pleg_position:
                if (self.leg_x1 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.vx = -self.vx - 3
                    self.vy = -self.vy - 1
                elif (self.leg_x1 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.vx = -self.vx - 3
                    self.vy = -self.vy - 1
                elif (self.leg_x2 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.vx = -self.vx - 3
                    self.vy = -self.vy - 1
                elif (self.leg_x2 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.vx = -self.vx - 3
                    self.vy = -self.vy - 1
                
        elif self.leg_position == 2: #28 * 20
            self.leg_x1 = self.player.x - 22
            self.leg_x2 = self.leg_x1 + 28
            if self.player.n == 2:
                self.leg_x1 = self.player.x + 22
                self.leg_x2 = self.leg_x1 - 28
            self.leg_y1 = self.player.y + self.player.r
            self.leg_y2 = self.leg_y1 + 20
            
            if self.leg_position > self.pleg_position:
                if (self.leg_x1 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 10
                    else: 
                        self.vy = self.vy - 10
                elif (self.leg_x1 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 10
                    else: 
                        self.vy = self.vy - 10
                elif (self.leg_x2 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 10
                    else: 
                        self.vy = self.vy - 10
                elif (self.leg_x2 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 10
                    else: 
                        self.vy = self.vy - 10
                        
            else:
                if (self.leg_x1 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x1 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x2 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x2 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                
        elif self.leg_position == 3: #30 * 23
            self.leg_x1 = self.player.x - self.player.r - 10
            self.leg_x2 = self.leg_x1 + 30
            if self.player.n == 2:
                self.leg_x1 = self.player.x + self.player.r + 10
                self.leg_x2 = self.leg_x1 - 30
            self.leg_y1 = self.player.y + self.player.r - 4
            self.leg_y2 = self.leg_y1 + 23
            
            if self.leg_position > self.pleg_position:
                if (self.leg_x1 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 17
                    else: 
                        self.vy = self.vy - 17
                elif (self.leg_x1 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 17
                    else: 
                        self.vy = self.vy - 17
                elif (self.leg_x2 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 17
                    else: 
                        self.vy = self.vy - 17
                elif (self.leg_x2 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 17
                    else: 
                        self.vy = self.vy - 17
            else:
                if (self.leg_x1 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x1 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x2 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x2 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                    
        elif self.leg_position == 4: #28 * 23
            self.leg_x1 = self.player.x - self.player.r - 20
            self.leg_x2 = self.leg_x1 + 28
            if self.player.n == 2:
                self.leg_x1 = self.player.x + self.player.r + 20
                self.leg_x2 = self.leg_x1 - 28
            self.leg_y1 = self.player.y + self.player.r - 17
            self.leg_y2 = self.leg_y1 + 23
            
            if self.leg_position > self.pleg_position:
                if (self.leg_x1 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 15
                    else: 
                        self.vy = self.vy - 15
                elif (self.leg_x1 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 15
                    else: 
                        self.vy = self.vy - 15
                elif (self.leg_x2 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 15
                    else: 
                        self.vy = self.vy - 15
                elif (self.leg_x2 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 10
                    else:
                        self.vx = self.vx - 10
                    if self.vy > 0:
                        self.vy = -self.vy - 15
                    else: 
                        self.vy = self.vy - 15
            else:
                if (self.leg_x1 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x1 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x2 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x2 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                    
        elif self.leg_position == 5: #28 * 23
            self.leg_x1 = self.player.x - self.player.r - 20
            self.leg_x2 = self.player.x - self.player.r + 7
            if self.player.n == 2:
                self.leg_x1 = self.player.x + self.player.r + 20
                self.leg_x2 = self.player.x + self.player.r - 7
            self.leg_y1 = self.player.y + 12
            self.leg_y2 = self.leg_y1 + 23
            
            if self.leg_position > self.pleg_position:
                if (self.leg_x1 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 15
                    else:
                        self.vx = self.vx - 15
                    if self.vy > 0:
                        self.vy = -self.vy - 20
                    else: 
                        self.vy = self.vy - 20
                elif (self.leg_x1 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 15
                    else:
                        self.vx = self.vx - 15
                    if self.vy > 0:
                        self.vy = -self.vy - 20
                    else: 
                        self.vy = self.vy - 20
                elif (self.leg_x2 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 15
                    else:
                        self.vx = self.vx - 15
                    if self.vy > 0:
                        self.vy = -self.vy - 20
                    else: 
                        self.vy = self.vy - 20
                elif (self.leg_x2 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    if self.vx > 0:
                        self.vx = -self.vx - 15
                    else:
                        self.vx = self.vx - 15
                    if self.vy > 0:
                        self.vy = -self.vy - 20
                    else: 
                        self.vy = self.vy - 20
            else:
                if (self.leg_x1 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x1 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x2 - self.x)**2 + (self.leg_y1 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
                elif (self.leg_x2 - self.x)**2 + (self.leg_y2 - self.y)**2 < self.r**2:
                    self.leg_kick.rewind()
                    self.leg_kick.play()
                    self.vx = -self.vx 
                    self.vy = -self.vy
        if self.player.n == 2:
            self.vx = -self.vx                         
    
    #player hits the ball with his head
    def player_ball(self, player):
        self.player = player
        dx = (self.x + 2*self.player.x)/3
        dy = (self.y + 2*self.player.y)/3
        
        if (dx - self.player.x)**2 + (dy - self.player.y)**2 <= self.r**2:
            self.head_kick.rewind()
            self.head_kick.play()
            if self.motion_v == False and self.player.vx == 0 and self.vx != 0 and self.vy == 0:
                if self.vx > 0:
                    self.vx = -self.vx - 1
                elif self.vx < 0:
                    self.vx = -self.vx + 1

            elif self.motion_v == False:
                self.vx = self.player.vx
                self.motion_h = True
                
            elif self.motion_v == True and self.vx == 0 and self.player.vx == 0:
                if dx == self.player.x:
                    self.vy = -self.vy + self.player.vy
                    if self.vy > 0:
                        self.vy = -self.vy
                    if self.vy > -2:
                        self.vy = 0
                if dx < self.player.x:
                    distance = math.sqrt((self.player.x - dx)**2 + (self.player.y - self.player.r/2 - dy)**2)
                    cos_angle = abs((distance**2 - 2*((self.player.r/2)**2))/(-2*((self.player.r/2)**2)))
                    if cos_angle > 2:
                        angle = 180
                    else:
                        angle = (math.acos(cos_angle))*(180/math.pi)
            
                    self.vx = -10 * ((angle / 90)) + self.player.vx
                    self.vy = -self.vy + self.player.vy
                elif dx > self.player.x:
                    distance = math.sqrt((self.player.x - dx)**2 + (self.player.y - self.player.r/2 - dy)**2)
                    cos_angle = abs((distance**2 - 2*((self.player.r/2)**2))/(-2*((self.player.r/2)**2)))
                    angle = (math.acos(cos_angle))*(180/math.pi)
                    if cos_angle > 2:
                        angle = 180
                    else:
                        angle = (math.acos(cos_angle))*(180/math.pi)
       
                    self.vx = 10 * ((angle / 90)) + self.player.vx
                    if self.vy < 0:
                        self.vy = self.vy
                    else:
                        self.vy = -self.vy + self.player.vy
            else:
                self.vx = self.player.vx
                if self.y + self.r < self.g and self.x <= self.player.x:
                    self.vx = -6 + self.player.vx
                    vy = self.vy
                    self.vy = -self.vy + self.player.vy
                    if self.player.vy != 0:
                        self.vy = self.vy - 5
                    if self.player.vx != 0:
                        self.vx = self.vx - 6
                if self.y + self.r < self.g and self.x > self.player.x:
                    self.vx = 6 + self.player.vx
                    self.vy = -self.vy + self.player.vy
                    if self.player.vy != 0:
                        self.vy = self.vy - 5
                    if self.player.vx != 0:
                        self.vx = self.vx + 6
                if self.y - self.r <= self.player.y + self.player.r and self.player.y + self.player.r != self.g:
                    if self.x >= self.player.x:
                        self.x = self.x + self.player.r/2
                        self.vx = 5
                    elif self.x < self.player.x:
                        self.x = self.x - self.player.r/2
                        self.vx = -5
                    
    #when player presses the ball 
    def player_over_ball(self, player):
        self.player = player
        dx = (self.x + 2*self.player.x)/3
        dy = (self.y + 2*self.player.y)/3
        
        if (dx - self.player.x)**2 + (dy - self.player.y)**2 <= self.r**2 and self.y - self.r <= self.player.y + self.player.r and self.player.y + self.player.r != self.player.g:
            if self.x > self.player.x:
                self.vx = 3
                self.motion_h = True
                self.x = self.player.x + self.player.r + self.r/2
            elif self.x <= self.player.x:
                self.vx = -3
                self.motion_h = True
                self.x = self.player.x - self.player.r - self.r/2
            
    def update(self):
        self.gravity()  
        self.net_ball()
        self.player_over_ball(game.player1)
        self.player_over_ball(game.player2)
        self.player_ball(game.player1)
        self.player_ball(game.player2)
        self.player_ball_kick(game.player1)
        self.player_ball_kick(game.player2)
        
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        
        #game area boundries
        if self.x - self.r < 0:
            self.vx = -self.vx
        if self.x + self.r > 1200:
            self.vx = -self.vx
        if self.y - self.r < 0:
            self.vy = -self.vy
            
    def display(self):
        self.update()
        
        #scrolling the ball horizontally
        image(self.img, self.x - self.r, self.y - self.r, self.r*2, self.r*2)
        if self.vx > 0:
            if self.img_n < 5:
                self.img_n = self.img_n + 1
            else:
                self.img_n = 1
            self.img = loadImage(path + "/images/" + "ball" + str(self.img_n) + ".png")
            image(self.img, self.x - self.r, self.y - self.r, self.r*2, self.r*2)
        elif self.vx < 0:
            if self.img_n > 1:
                self.img_n = self.img_n - 1
            else:
                self.img_n = 5
            self.img = loadImage(path + "/images/" + "ball" + str(self.img_n) + ".png")
            image(self.img, self.x - self.r, self.y - self.r, self.r*2, self.r*2)
            
            
class Net:
    def __init__(self, n):
        self.w = NET_WIDTH
        self.h = NET_HEIGHT
        self.netnumber = n
        self.score = 0
        self.img = loadImage(path + "/images/" + "net"+ str(self.netnumber) + ".png")
    
    #checking for goal
    def goal(self):
        self.ball = game.ball
        if self.ball.x < 130 and self.ball.y > 485 and game.player1.goal == False and game.player2.goal == False:
            game.background_sound.rewind()
            game.goal_sound.rewind()
            game.goal_sound.play()
            game.net_sound.rewind()
            game.net_sound.play()
            game.player1.goal = True
            game.seconds = time.time()
        elif self.ball.x > 1070 and self.ball.y > 485 and game.player1.goal == False and game.player2.goal == False:
            game.goal_sound.rewind()
            game.goal_sound.play()
            game.net_sound.rewind()
            game.net_sound.play()
            game.player2.goal = True
            game.seconds = time.time()
    
    def display(self):
        self.goal()
        if self.netnumber == 2:
            image(self.img, 0, 480, self.w, self.h)
        elif self.netnumber == 1:
            image(self.img, 1072, 480, self.w, self.h)

class Game:
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.t = ''
        self.seconds = 0
        self.stop = 0
        self.stadium_shaking = 0
        self.one_second = 1
        self.player1 = Player(1000, GROUND - PLAYER_RADIUS, PLAYER_RADIUS, GROUND, 1)
        self.player2 = Player(200, GROUND - PLAYER_RADIUS, PLAYER_RADIUS, GROUND, 2)
        self.ball = Ball(30, 0, BALL_RADIUS, GROUND)
        self.net1 = Net(1)
        self.net2 = Net(2)
        
        self.background_sound = player.loadFile(path + "/sounds/background.mp3")
        self.net_sound = player.loadFile(path + "/sounds/net_goal.mp3")
        self.goal_sound = player.loadFile(path + "/sounds/SUIII.mp3")
        self.field_img = loadImage(path + "/images/" + "field.png")
        self.stadium_img = loadImage(path + "/images/" + "stadium.png")
        self.table_img = loadImage(path + "/images/" + "table.png")
    
    #complex interaction between 3 objects (player-ball-player)
    def player_ball_player(self, player_l, player_r):
        self.player_ball_l = player_l
        self.player_ball_r = player_r
        
        dx_p1 = (self.ball.x + 2*self.player_ball_l.x)/3
        dy_p1 = (self.ball.y + 2*self.player_ball_l.y)/3
        
        dx_p2 = (self.ball.x + 2*self.player_ball_r.x)/3
        dy_p2 = (self.ball.y + 2*self.player_ball_r.y)/3
        
        dx = (self.player_ball_r.x + self.player_ball_l.x)/2
        dy = (self.player_ball_r.y + self.player_ball_l.y)/2
        
        if self.player_ball_l.x < self.ball.x < self.player_ball_r.x and self.ball.vy == 0:
            if (dx_p1 - self.player_ball_l.x)**2 + (dy_p1 - self.player_ball_l.y)**2 <= self.ball.r**2 and (dx_p2 - self.player_ball_r.x)**2 + (dy_p2 - self.player_ball_r.y)**2 <= self.ball.r**2:
                    choice = random.randint(1,2)
                    if choice == 1:
                        self.ball.x = dx
                        self.player_ball_r.x = self.ball.x + 45
                        self.player_ball_l.x = self.ball.x - 45
                        self.player_ball_l.vy = -7
                        self.player_ball_l.vx = 7
                    elif choice == 2:
                        self.ball.x = dx
                        self.player_ball_r.x = self.ball.x + 45
                        self.player_ball_l.x = self.ball.x - 45
                        self.player_ball_r.vy = -7
                        self.player_ball_r.vx = -7

    
    def display(self):
        
        image(self.stadium_img, 0, -100)
        image(self.field_img, 0, 595)
        image(self.table_img, 185, 710, 827, 90)
        
        self.player1.display()
        self.player2.display()
        self.ball.display()
        self.net1.display()
        self.net2.display()
        self.player_ball_player(self.player2, self.player1)
        
        textSize(25)
        fill(255,255,255)
        text(str(self.net1.score) + " - ", 570, 750)
        text(str(self.net2.score), 615, 750)
        
        
game = Game(WIDTH, HEIGHT, GROUND)

def setup():
    background(119, 198, 110)
    size(WIDTH, HEIGHT)
def draw():
    game.background_sound.play()
    
    game.stop = time.time()
    game.display()
    # if one of them scores a goal
    if game.player1.goal == True or game.player2.goal == True:
        fill(0, 0, 0)
        strokeWeight(0)
        rect(0, 0, 1200, 800)
        image(game.stadium_img, 0, -100)
        if game.stadium_shaking == 0 and frameCount % 6 == 0:
            image(game.stadium_img, -15, -115)
            game.stadium_shaking = 1
        elif frameCount % 6 == 0:
            image(game.stadium_img, 15, -85)
            game.stadium_shaking = 0
        image(game.field_img, 0, 595)
        if game.stadium_shaking == 0 and frameCount % 4 == 0:
            textSize(60)
            fill(255, 0, 0)
            text("GOAAAAAAAAL!!!", 355, 780)
            game.stadium_shaking = 1
        elif frameCount % 4 == 0:
            textSize(60)
            fill(255, 0, 0)
            text("GOAAAAAAAAL!!!", 355, 780)
            game.stadium_shaking = 0
        if game.player1.goal == True:
            game.player1.display()
        elif game.player2.goal == True:
            game.player2.display()            
        game.ball.display()
        game.net1.display()
        game.net2.display()
        
        game.stop = time.time()
        #after celebration 3 seconds
        if game.stop - game.seconds > 3:
            tint(255, 255)
            if game.player1.goal == True:
                game.net2.score = game.net2.score + 1
            elif game.player2.goal == True:
                game.net1.score = game.net1.score + 1
            game.player1.goal = False
            game.player2.goal = False
            game.ball = Ball(30, 0, BALL_RADIUS, GROUND)
            game.player1 = Player(1000, GROUND - PLAYER_RADIUS, PLAYER_RADIUS, GROUND, 1)
            game.player2 = Player(200, GROUND - PLAYER_RADIUS, PLAYER_RADIUS, GROUND, 2)
            
    #the game continues until one of them scores 7 goals
    if game.net1.score > 6:
        image(game.stadium_img, 0, -100)
        image(game.field_img, 0, 595)
        image(game.table_img, 185, 710, 827, 90)
        game.player2.display()
        game.net1.display()
        game.net2.display()
        
        textSize(60)
        fill(255, 0, 0)
        text("Real Madrid won!!!", 350, 200)
        text(str(game.net1.score) + " - " + str(game.net2.score), 530, 300)
        textSize(30)
        fill(255, 0, 0)
        text("Press the mouse to restart the game", 450, 400)
    elif game.net2.score > 6:
        image(game.stadium_img, 0, -100)
        image(game.field_img, 0, 595)
        image(game.table_img, 185, 710, 827, 90)
        game.player1.display()
        game.net1.display()
        game.net2.display()
        textSize(60)
        fill(255, 0, 0)
        text("Manchester United won!!!", 400, 200)
        text(str(game.net1.score) + " - " + str(game.net2.score), 550, 300)
        textSize(30)
        fill(255, 0, 0)
        text("Press the mouse to restart the game", 450, 400)
        
    
def mouseClicked():
    #mouseclicked to restart the match
    if game.net1.score > 6 or game.net2.score > 6:
        game.t = ''
        game.seconds = 0
        game.stop = 0
        game.stadium_shaking = 0
        game.one_second = 1
        game.player1 = Player(1000, GROUND - PLAYER_RADIUS, PLAYER_RADIUS, GROUND, 1)
        game.player2 = Player(200, GROUND - PLAYER_RADIUS, PLAYER_RADIUS, GROUND, 2)
        game.ball = Ball(30, 0, BALL_RADIUS, GROUND)
        game.net1 = Net(1)
        game.net2 = Net(2)
    

#game control
def keyPressed():
    if keyCode == LEFT:
        if game.player1.left == True:
            game.player1.key_handler[LEFT] = True
            game.player1.key_handler[RIGHT] = False
    elif keyCode == RIGHT:
        if game.player1.right == True:
            game.player1.key_handler[LEFT] = False
            game.player1.key_handler[RIGHT] = True
    elif keyCode == UP:
        if game.player1.up == True:
            game.player1.key_handler[UP] = True
    if key == 'p' or key == 'P':
        if game.player1.kick == True:
            game.player1.key_handler['Kick'] = True

    if key == 'a' or key == 'A':
        if game.player2.left == True:
            game.player2.key_handler[LEFT] = True
            game.player2.key_handler[RIGHT] = False
    elif key == 'd' or key == 'D':
        if game.player2.right == True:
            game.player2.key_handler[LEFT] = False
            game.player2.key_handler[RIGHT] = True
    elif key == 'w' or key == 'W':
        if game.player2.up == True:
            game.player2.key_handler[UP] = True
    if key == 'c' or key == 'C':
        if game.player2.kick == True:
            game.player2.key_handler['Kick'] = True
        
def keyReleased():
    if keyCode == LEFT:
        game.player1.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.player1.key_handler[RIGHT] = False
    elif keyCode == UP:
        game.player1.key_handler[UP] = False
    if key == 'p' or key == 'P':
        game.player1.key_handler['Kick'] = False
    
    if key == 'a' or key == 'A':
        game.player2.key_handler[LEFT] = False
    elif key == 'd' or key == 'D':
        game.player2.key_handler[RIGHT] = False
    elif key == 'w' or key == 'W':
        game.player2.key_handler[UP] = False
    if key == 'c' or key == 'C':
        game.player2.key_handler['Kick'] = False
