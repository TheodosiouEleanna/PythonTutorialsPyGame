import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800 #screen width
s_height = 700 #screen height
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30 

top_left_x = (s_width - play_width) // 2 #top left position of play area
top_left_y = s_height - play_height #


# SHAPE FORMATS

S = [['.....', #lists of posible rotations
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T] # each one is a list of lists of possible shapes
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    rows = 20  # y
    columns = 10  # x
    
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 # number from 0-3


def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)] #creating one list for every row in the grid (20 sublists)   
    #2-D list 
    # (0,0,0) = black
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions: 
                c = locked_positions[(j,i)]
                grid[i][j] = c #looking through the grid and finding the corresponding position for the locked position to change the color in the grid
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] #getting the shape from the shape list and the sublist of posible rotations
    #rotations % (mod) the number of items in the list of shape rotations gives us the specific shape (0, 1, 2, 3)

    for i, line in enumerate(format): #looping through a certain shape with '.' and '0'
        row = list(line) #list of enumerated lines in the certain shape is rows
        for j, column in enumerate(row): #enumarated rows is columns
            if column == '0': #if a '0' exists
                positions.append((shape.x + j, shape.y + i)) #we add the position of the 0 into the list positions
        
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) #offsetting so shapes spawn above the screen in position -1 or -2

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range (10) if grid[i][j] == (0, 0, 0)] for i in range (20)] #going from this [[(0,1)],[(0,2)]]
    #if explained : only adding posiiton if the position is empty
    accepted_pos = [j for sub in accepted_pos for j in sub] #taking the 2-D positions of the list and adding them into an 1-D list #to this [(0,1), (0,2)]

    formatted = convert_shape_format(shape) # list that looks like this [(0,2), (2,3)]

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1]>-1: #if the shape spawns in pos value grater than -1 its not a valid position
                return False
    return True


def check_lost(positions):
    for pos in positions: 
        x, y = pos
        if y <1:
            return True
    return False


def get_shape():
    global shapes, shape_colors
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold = True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2)) #middle position of where we should be drawing in terms of x coordinate


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    #draws 20 vertical lines and 10 horizontal lines
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*block_size), (sx + play_width, sy + i* block_size)) #draw.line args: (surface, color, start_pos(x,y), end_pos(x,y))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy), (sx + j*block_size ,sy + play_height)) #draw.line: (surface, color, (start_pos, end_pos), width)



def clear_rows(grid, locked_positions):
    inc = 0
    for i in range(len(grid) - 1, -1, -1): #looping through the grid backwards
        row = grid[i]
        if (0, 0, 0) not in row: #if there are no black sqaures in a row it means that it is filled with shapes
            inc += 1
            ind = i #indicades the row position we want to delete
            for j in range(len(row)):
                try:
                    del locked_positions[(j, i)]
                except:
                    continue

    if inc > 0: #means that we have deleted at least 1 row
        for key in sorted(list(locked_positions), key=lambda x: x[1])[::-1]: # key = lamda x: x[1] :sorts list of locked positions based on the y value 
            x, y = key # getting the x,y value of every key in locked positions
            if y < ind: #we wanna shift every position down by 1. if y value is less than the row that we deleted
                newKey = (x, y + inc) # we give a new position with the y value incremented by the number of rows we have deleted to shift it down
                locked_positions[newKey] = locked_positions.pop(key) # creating new key in locked_positions which is gonna have the same color value as the last key
                #locked_positions.pop(key): gives us the last color value and is equal to the (x, y + inc) position

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50 #moving more to the right
    sy = top_left_y + play_height/2 - 100 #moving more downwards
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size))

    surface.blit(label, (sx + 10, sy - 30)) #draws the label 


def update_score(nscore):
    score = max_score()
    
    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore)) #writing on the txt file either the new or the old high score

def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip() #removes \n from text file
    
    return score


def draw_window(surface, grid, score = 0, last_score = 0):
    surface.fill((0,0,0))
    #Tetris Title
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 30))

    #current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score : ' + str(score) , 1, (255, 255, 255))

    sx = top_left_x + play_width + 50 #moving more to the right
    sy = top_left_y + play_height/2 - 100 #moving more downwards

    surface.blit(label, (sx + 10, sy + 160))
    
    #last score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('High Score : ' + last_score , 1, (255, 255, 255))

    sx = top_left_x - 190 #moving more to the right
    sy = top_left_y + 200 #moving more downwards

    surface.blit(label, (sx + 10, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0) 
            #loop through every color in the grid (grid[i][j]=color) and drawing the cube in the specific position

    draw_grid(surface, grid) # draw grid and border
    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 5)
    #draws the actual grid 
    
    
def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid (locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0


    while run: 

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 >= fall_speed: #
            fall_time = 0
            current_piece.y += 1 # moving down the piece by one
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True #either we have hit the bottom of the screen or an other piece

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape) 
                elif event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece) #convert_shape_format returns the formatted of positions of the pieces 

        for i in range(len(shape_pos)): #shape_pos is a list of the formatted positions of the shape
            x, y = shape_pos[i]
            if y > -1: #so that we are not above the screen
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color # locked_positions is a dictionary with the p position an the value of the color like: {(1,2):(255, 0 ,0)}
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
    
        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):       
            run = False
    
    draw_text_middle("You Lost", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)  
    update_score(score)

def main_menu(win):
    run = True 
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press Any Key To Play', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game