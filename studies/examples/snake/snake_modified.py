'''
Transcribed by Sami Rami from tutorials :
https://www.youtube.com/playlist?list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
Conversion to .app made with py2app for distribution
'''
import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (111, 195, 223)
# New colours added
tron_blue = (106, 243, 243)
tron_blue2 = (198, 241, 240)

# 

display_width = 800
display_height = 600

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tron Grid')

icon_img = pygame.image.load('images/apple.png')
pygame.display.set_icon(icon_img)

head_img = pygame.image.load('images/tron.png')
head_img = pygame.transform.scale(head_img, (30, 30))
head_width = 73
head_height = 73
head = pygame.transform.scale(head_img, (head_width, head_height))
apple_img = pygame.image.load('images/apple.png')

clock = pygame.time.Clock()

apple_thickness = 30
block_size = 10
fps = 15

direction = 'right'

small_font = pygame.font.SysFont('helvetica', 25)
med_font = pygame.font.SysFont('helvetica', 50)
large_font = pygame.font.SysFont('helvetica', 80)

def pause():

     paused = True

     message_to_screen("Paused", tron_blue, -100, 'large')
     message_to_screen("Press C to continue or Q to quit", tron_blue2, 25)

     pygame.display.update()

     while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        #game_display.fill(white)
        
        clock.tick(5)
            


def score(score):
    text = small_font.render("Score: " + str(score), True, black)
    game_display.blit(text, [0,0])

def rand_apple_gen():
    rand_apple_x = round(random.randrange(0, display_width - apple_thickness))
    rand_apple_y = round(random.randrange(0, display_height - apple_thickness))

    return rand_apple_x, rand_apple_y


def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        game_display.fill(black)
        # Welcome message changed
        message_to_screen("Welcome to Tron Grid", tron_blue, -100, 'large')
        message_to_screen("The objective of the game is to defeat your"
                          + " opponent", tron_blue2, -30)
        message_to_screen("Power-ups will help you become more powerful", tron_blue2, 10)
        message_to_screen("If you run into yourself or the other player's trail"
                          +" you die!", tron_blue2, 50)
        message_to_screen("Press C to play, P to pause or Q to quit", tron_blue2, 180)

        pygame.display.update()
        clock.tick(5)

def snake(block_size, snake_list):

    if direction == 'right':
        head = pygame.transform.rotate(head_img, 270)
    elif direction == 'left':
        head = pygame.transform.rotate(head_img, 90)
    elif direction == 'up':
        head = head_img
    elif direction == 'down':
        head = pygame.transform.rotate(head_img, 180)
    
    game_display.blit(head, (snake_list[-1][0]-10, snake_list[-1][1]))
    
    for x_y in snake_list[:-1]:
        game_display.fill(tron_blue, rect=[x_y[0], x_y[1]+10, block_size, block_size])


def text_objects(text, color, size):
    if size == 'small':
        text_surface = small_font.render(text, True, color)
    elif size == 'medium':
        text_surface = med_font.render(text, True, color)
    elif size == 'large':
        text_surface = large_font.render(text, True, color)
        
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace = 0, size = 'small'):
    text_surf, text_rect = text_objects(msg, color,size)
    text_rect.center = (display_width / 2), (display_height / 2) + y_displace
    game_display.blit(text_surf, text_rect)

snake_list = []
def game_loop():

    global direction

    direction = 'right'
    
    game_exit = False
    game_over = False

    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 10
    lead_y_change = 0

    snake_list = []
    snake_length = 100

    rand_apple_x, rand_apple_y = rand_apple_gen()
    
    while not game_exit:

        if game_over == True:
            message_to_screen("Game over", red, -50, 'large')
            message_to_screen("press C to play again or Q to quit", black, 50, 'medium')
            pygame.display.update()
              
        while game_over == True:
            #game_display.fill(white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    elif event.key == pygame.K_c:
                        game_loop()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                prev_dir = direction
                if event.key == pygame.K_LEFT and prev_dir != 'right':
                    direction = 'left'
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT and prev_dir != 'left':
                    direction = 'right'
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP and prev_dir != 'down':
                    direction = 'up'
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN and prev_dir != 'up':
                    direction = 'down'
                    lead_y_change =block_size
                    lead_x_change = 0
                    
                elif event.key == pygame.K_p:
                    pause()
        # Code added to accomplish task of not running into walls but
        # appearing on other side instead.
        
        if lead_x >= display_width:
             lead_x = 0
        if lead_x < 0:
             lead_x = display_width
        if lead_y >= display_height:
             lead_y = 0
        if lead_y < 0:
             lead_y = display_height
             # game_over = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        
        game_display.fill(black)
        game_display.blit(apple_img, (rand_apple_x, rand_apple_y))
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True
        
        snake(block_size, snake_list)

        score(snake_length - 1)
        
        pygame.display.update()

        if lead_x > rand_apple_x and lead_x < rand_apple_x + apple_thickness \
           or lead_x + block_size > rand_apple_x and lead_x + block_size < rand_apple_x + apple_thickness:

            if lead_y > rand_apple_y and lead_y < rand_apple_y + apple_thickness:

                rand_apple_x, rand_apple_y = rand_apple_gen()
                snake_length += 1

            elif lead_y + block_size > rand_apple_y and lead_y + block_size < rand_apple_y + apple_thickness:

                rand_apple_x, rand_apple_y = rand_apple_gen()
                snake_length += 1

        clock.tick(fps)

    pygame.quit()
    quit()

game_intro()
game_loop()
