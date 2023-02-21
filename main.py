import pygame
from random import randint


# Init the game
pygame.init()

# Define the game speed
score = 0
speed = 15 + score

# Define the window
w = 640
h = 480
wind = pygame.display.set_mode((w, h))

bg_color = pygame.Color(0,0,0)


# Init the playground
squares_x = 32
squares_y = 24

square_w = w // squares_x
square_h = h // squares_y


# Init the food
food = [squares_x//2, squares_y//2]


# Init the snake
snake_x, snake_y = squares_x // 4, squares_y //2
INITIAL_LENGTH = 3
snake = [
    [snake_x, snake_y],
    [snake_x-1, snake_y],
    [snake_x-2, snake_y]
]


def drawFood():
    food_color = pygame.Color(255,0,0)
    food_draw = pygame.Rect((food[0]*square_w, food[1]*square_h), (square_w, square_h))
    pygame.draw.rect(wind, food_color, food_draw)


def drawSnake():
    snake_color = pygame.Color(0,255,0)
    for cell in snake:
        cell_rect = pygame.Rect((cell[0]*square_w, cell[1]*square_h), (square_w, square_h))
        pygame.draw.rect(wind, snake_color, cell_rect)


# Update the Snake direction
def updateSnake(direction):
    global food, speed, score
    x, y = direction
    head = snake[0].copy()
    head[0] = (head[0]+x)
    head[1] = (head[1]+y)

    # Check if the game is over
    if head in snake[1:] or head[0] < 0 or head[0] >= squares_x or head[1] < 0 or head[1] >= squares_y:
        return False
    elif head == food:
        speed += 1
        score += 1
        food = None
        while food is None:
            newfood = [
                randint(5, squares_x-5),
                randint(5, squares_y-5)
            ]
            food = newfood if newfood not in snake else None

    else:
        snake.pop()

    snake.insert(0, head)
    return True


def game_over():

    global score

    print_text = 0
    new_name = []
    screen_res = (w,h)
    screen = pygame.display.set_mode(screen_res)
    pygame.display.set_caption("Game Over")

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.KEYDOWN:
                        if (event.unicode >= 'a' and event.unicode <= 'z') or (event.unicode >= 'A' and event.unicode <= 'Z'):
                            letter = event.unicode
                            new_name.append(letter)
            if pygame.mouse.get_pressed() == (1, 0, 0) and (x > 230 and y > 70 and x < 390 and y < 300):
                        print_text = 1
                        if new_name != []:
                            with open ('score.txt', 'a') as file:  
                                file.write(''.join(new_name) + " : " + str(score) + '\n')
                        else:
                            pass
                        

        if print_text == 0:

            x,y = pygame.mouse.get_pos()
            high_score_label = pygame.font.Font(None, 50).render("Highest Score : " + str(score), 1, (255, 255, 255))
            screen.blit(high_score_label, (170, 50))
            
            enter_your_name_label = pygame.font.Font(None, 30).render("Please enter your name", 1, (255, 255, 255))
            screen.blit(enter_your_name_label, (190, 100))
            
            printed_new_word = pygame.font.Font(None, 40).render(''.join(new_name), True, (0, 255, 0))
            screen.blit(printed_new_word, (270, 180))

            save_score = pygame.font.Font(None, 40).render("Save score", True, (255, 255, 255))
            screen.blit(save_score, (240, 275))
        
        if print_text == 1:
            hall_of_fame_label = pygame.font.Font(None, 50).render("Hall of fame : ", 1, (255, 255, 255))
            screen.blit(hall_of_fame_label, (210, 50))
            i = 0
            with open('score.txt', 'r') as file:
                        scores = file.readlines()
            if len(scores) < 5:
                while i < len(scores):
                    scores[i] = scores[i][:-1]
                    printed_new_word = pygame.font.Font(None, 40).render(str(scores[i]), True, (0, 255, 0))
                    screen.blit(printed_new_word, (250, 120 + i*50))
                    i += 1
            else:
                while i < 5 and len(scores) >= 5:
                    scores[i] = scores[i][:-1]
                    printed_new_word = pygame.font.Font(None, 40).render(str(scores[i]), True, (0, 255, 0))
                    screen.blit(printed_new_word, (250, 120 + i*50))
                    i += 1

        pygame.display.flip()


# Game loop
running = True
direction = [1,0]
while running:
    pygame.time.Clock().tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_RIGHT and not direction == [-1,0]:
                direction = [1,0]
            if event.key == pygame.K_LEFT and not direction == [1,0]:
                direction = [-1,0]
            if event.key == pygame.K_UP and not direction == [0,1]:
                direction = [0,-1]
            if event.key == pygame.K_DOWN and not direction == [0,-1]:
                direction = [0,1]

    # Game over conditon
    if updateSnake(direction) == False:
        game_over()
        running = False

    # Draw the game
    wind.fill(bg_color)
    drawFood()
    drawSnake()

    pygame.display.update()

pygame.quit()