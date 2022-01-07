import pygame


from pygame.math import Vector2 as vec
#screen setting
WIDTH = 610
HEIGHT = 670

FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_HEIGHT = HEIGHT - TOP_BOTTOM_BUFFER
MAZE_WIDTH = WIDTH - TOP_BOTTOM_BUFFER

ROWS = 30
COLS = 28

#color setting
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
BLUE = (65, 105, 225)
RED = (208, 22, 22)
GREY = (128, 128 ,128)
GREEN = (0, 100, 0)
PINK = (255, 102, 153)
PLAYER_COLOR = (255, 215, 0)
SKY = (65, 105, 225)

#image setting
PACMAN_LOGO = pygame.image.load("PACMAN_LOGO_SMALL_1.png")
GAME_OVER_LOGO = pygame.image.load("GAME_OVER_LOGO.png")
WINNER_LOGO = pygame.image.load("WINNER_LOGO_2.png")

#font setting
START_TEXT_SIZE = 30
START_FONT = "emulogic.ttf"
OVER_FONT = "PixelMiners-KKal"


#player setting
#PLAYER_START_POS = (2,2)

#mob setting