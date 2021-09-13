#Snake Game
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)): 
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) #changing position
        #grid 20x20

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = [] #list
    turns = {} #dictionary
    def __init__(self, color, pos): #constructor of object snake
        self.color = color 
        self.head = cube(pos) #pos=tuple
        self.body.append(self.head)# adds head to the body list
        self.dirnx = 0 #direction for x 
        self.dirny = 1 #direction for y 


    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #quit button
                pygame.quit()
 
            keys = pygame.key.get_pressed() #dictionary with all the key values and if they are pressed or not (you can click multiple)
 
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1 #moving left
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                     #list of adding a #key of the current head position of the snake equal to what direction we turn
                    #added the potiion of the turn
 
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
        for i, c in enumerate(self.body): #look through the list of positions that we having
            p = c.pos[:] # [:] makes a copy so it does not change the position of the snake
            #for each object c (who have a position) 
            if p in self.turns: #if p in list of positions then we gonna turn
                turn = self.turns[p] #find the direction value through index p
                c.move(turn[0],turn[1]) #giving direction x and y so it knows what way it needs to move
                if i == len(self.body)-1:  #if we are on the last cube 
                    self.turns.pop(p) # we remove that turn
            else:
            #checking whether or not we ve reached the edge of the screen
                    #if we are moving left and the x position of cube is less or equal to zero, we change the position to go 
                    #in the right side of the screen
                    #giving the x position to be 19 and the y position to be 1
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny) #keep moving in the same direction it's going

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx , dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0: #if snake is moving to the right
            self.body.append(cube((tail.pos[0]-1, tail.pos[1]))) 
            #add a new cube to the body and its position is one less position to the x of that tail
        elif dx == -1 and dy == 0: #if snake is moving to the left
            self.body.append(cube((tail.pos[0]+1, tail.pos[1]))) #x and y
            #add a new cube to the body and its position is one more position to the x of that tail
        elif dx == 0 and dy == 1: #if snake is moving up
            self.body.append(cube((tail.pos[0], tail.pos[1]-1))) 
            #add a new cube to the body and its position is one less position to the y of that tail
        elif dx == 0 and dy == -1: #if snake is moving down
            self.body.append(cube((tail.pos[0], tail.pos[1]+1))) 
            #add a new cube to the body and its position is one more position to the y of that tail
        self.body[-1].dirnx = dx #what the tail is moving at that current moment
        self.body[-1].dirny = dy


    def draw (self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True) #true draws EYES
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows #
    x = 0
    y = 0
    
    for i in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0), (x,w)) #drawing line at 0 and w in every loop 
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y)) #start and end position of the line


def redrawWindow(surface):
    global rows, width, s, snack #redrawing all this
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width , rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body
 
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
       
    return (x,y)
        #get a list of a filtered list to see if any of the positions 
        #are the same with the current position of the snake so that we don't put a snack on top of the snake

def message_box(subject, content):
    root = tk.Tk() #new tkinter window
    root.attributes("-topmost", True) #put window on top of everything
    root.withdraw()#make window invisible
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width , rows, s, snack
    width = 500
    rows = 20
    s = 0
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0),(10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True

    clock = pygame.time.Clock() 

    while flag:
        pygame.time.delay(50) #ms
        clock.tick(10) #game runs <10 fps
        s.move()

        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color = (0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):  #looping through every cube of the snake
        #checking if the position is in the list of all the position after that
                print('Score:', len(s.body)) 
                message_box('You Lost!','Play again')
                s.reset((10,10))
                break

        redrawWindow(win) 
       
    pass


#rows =
#w =
#h = cube,rows = rows
#cube.w = w

main()