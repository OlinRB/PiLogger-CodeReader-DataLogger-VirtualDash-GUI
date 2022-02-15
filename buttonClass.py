#Original Author: https://github.com/russs123/pygame_button // youtube: https://www.youtube.com/channel/UCPrRY0S-VzekrJK7I7F4-Mg

import pygame
from pygame.locals import *


pygame.init()
pygame.font.init()


button_font = pygame.font.SysFont('agencyfb', 18)

# define colours
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 179, 138)
white = (255, 255, 255)
silver = (190, 190, 191)
orange = (252, 69, 19)
grey = (112, 128, 144)
# define global variable
clicked = False
counter = 0


class button():
    # colours for button and text - edited
    button_col = green
    hover_col = (17, 59, 18)
    click_col = (50, 150, 255)
    text_col = white
    width = 111
    height = 35

    # Constructor edited to take in screen parameter
    def __init__(self, x, y, text, screen):
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen


    def draw_button(self):

        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(self.screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(self.screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(self.screen, self.button_col, button_rect)

        # add shading to button
        pygame.draw.line(self.screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(self.screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(self.screen, orange, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(self.screen, orange, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = button_font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y/2 + 18))
        return action
