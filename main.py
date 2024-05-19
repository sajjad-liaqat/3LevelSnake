import pygame
import time
import random

pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
background_color = (240, 240, 245)  # Soft light grey with a hint of lavender
snake_color = (0, 204, 102)  # Vibrant green
food_color = (255, 69, 0)  # Striking red-orange
obstacle_color = (105, 105, 105)  # Cool dark grey
score_text_color = (30, 144, 255)  # Bright dodger blue
game_over_text_color = (220, 20, 60)  # Deep crimson
high_score_text_color = (255, 215, 0)  # Bright gold
message_text_color = (123, 104, 238)  # Medium slate blue

# Define display dimensions
dis_width = 800
dis_height = 600
top_margin = 80  # Space at the top for scores

# Load sounds
eat_sound = pygame.mixer.Sound('eat.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

# Create the display window
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Set the game clock
clock = pygame.time.Clock()
snake_block = 20

# Set fonts for text display
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Initialize high score
high_score = 0

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, snake_color, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - mesg.get_width() / 2, dis_height / 2 - mesg.get_height() / 2 + y_displace])

def your_score(score, high_score):
    value = score_font.render("Your Score: " + str(score), True, score_text_color)
    dis.blit(value, [10, 10])
    if high_score > 0:
        high_value = score_font.render("High Score: " + str(high_score), True, high_score_text_color)
        dis.blit(high_value, [10, 50])

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(dis, obstacle_color, [obstacle[0], obstacle[1], snake_block, snake_block])

def gameLoop():
    global high_score
    game_over = False
    game_close = False
    pause = False

    # Difficulty level selection
    difficulty = False
    while not difficulty:
        dis.fill(background_color)
        message("Select Difficulty: 1-Easy, 2-Medium, 3-Hard", message_text_color)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    snake_speed = 10
                    difficulty_level = "Easy"
                    difficulty = True
                elif event.key == pygame.K_2:
                    snake_speed = 15
                    difficulty_level = "Mid"
                    difficulty = True
                elif event.key == pygame.K_3:
                    snake_speed = 20
                    difficulty_level = "Hard"
                    difficulty = True

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    def spawn_food():
        return round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0, \
               round(random.randrange(top_margin, dis_height - snake_block - 50) / 20.0) * 20.0

    foodx, foody = spawn_food()

    obstacles = []
    for _ in range(5):
        obs_x = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
        obs_y = round(random.randrange(top_margin, dis_height - snake_block) / 20.0) * 20.0
        obstacles.append([obs_x, obs_y])

    while not game_over:

        while game_close:
            dis.fill(background_color)
            message("You Lost! Press Q-Quit or C-Play Again", game_over_text_color, 50)
            your_score(length_of_snake - 1, high_score)
            if length_of_snake - 1 > high_score:
                high_score = length_of_snake - 1
                message("New High Score! 🎉", high_score_text_color, 100)
            pygame.display.update()
            pygame.mixer.Sound.play(game_over_sound)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
                if not pause:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0

        if pause:
            continue

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(background_color)
        pygame.draw.rect(dis, food_color, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for obstacle in obstacles:
            if x1 == obstacle[0] and y1 == obstacle[1]:
                game_close = True

        our_snake(snake_block, snake_list)
        draw_obstacles(obstacles)
        your_score(length_of_snake - 1, high_score)

        # Display selected difficulty level
        level_text = score_font.render("Level: " + difficulty_level, True, score_text_color)
        dis.blit(level_text, [dis_width - 200, 10])

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            pygame.mixer.Sound.play(eat_sound)
            foodx, foody = spawn_food()
            length_of_snake += 1

        clock.tick(snake_speed)

    dis.fill(background_color)
    message("Game Over", game_over_text_color, -50)
    if length_of_snake - 1 > high_score:
        high_score = length_of_snake - 1
        message("New High Score! 🎉", high_score_text_color, 50)
    pygame.display.update()
    time.sleep(2)

    pygame.quit()
    quit()

gameLoop()
