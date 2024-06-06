#this version has used Chatgpt to optimize some mistakes.


import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Screen dimensions
SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936

# Game variables
GROUND_SCROLL = 0
SCROLL_SPEED = 4
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
FONT = pygame.font.SysFont('Bauhaus 93', 60)
WHITE = (255, 255, 255)

# Load images
BG_IMG = pygame.image.load('Images/background.png')
GROUND_IMG = pygame.image.load('Images/ground.png')
BUTTON_IMG = pygame.image.load('Images/replay.png')
BIRD_IMGS = [pygame.image.load(f'Images/bird{num}.png') for num in range(1, 4)]
PIPE_IMG = pygame.image.load('Images/pipe.png')


def draw_text(text, font, color, x, y, screen):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = BIRD_IMGS
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self, flying, game_over):
        if flying:
            self.vel += 0.5
            self.vel = min(self.vel, 8)
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not game_over:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            if self.counter > 5:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = PIPE_IMG
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - PIPE_GAP // 2]
        elif position == -1:
            self.rect.topleft = [x, y + PIPE_GAP // 2]

    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


def reset_game(pipe_group, bird):
    pipe_group.empty()
    bird.rect.x = 100
    bird.rect.y = SCREEN_HEIGHT // 2
    return 0


# Initialize game objects
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
flappy = Bird(100, SCREEN_HEIGHT // 2)
bird_group.add(flappy)
button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100, BUTTON_IMG)

# Game loop
run = True
flying = False
game_over = False
score = 0
last_pipe = pygame.time.get_ticks() - PIPE_FREQUENCY
pass_pipe = False

while run:
    clock.tick(fps)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.blit(BG_IMG, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update(flying, game_over)
    screen.blit(GROUND_IMG, (GROUND_SCROLL, 768))

    if flying and not game_over:
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > PIPE_FREQUENCY:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = current_time

        GROUND_SCROLL -= SCROLL_SPEED
        GROUND_SCROLL %= 35
        pipe_group.update()

    draw_text(str(score), FONT, WHITE, SCREEN_WIDTH // 2, 20, screen)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over and button.draw(screen):
        game_over = False
        score = reset_game(pipe_group, flappy)

    if not game_over and flying:
        if len(pipe_group) > 0:
            first_pipe = pipe_group.sprites()[0]
            if bird_group.sprites()[0].rect.left > first_pipe.rect.left \
                    and bird_group.sprites()[0].rect.right < first_pipe.rect.right \
                    and not pass_pipe:
                pass_pipe = True
            if pass_pipe and bird_group.sprites()[0].rect.left > first_pipe.rect.right:
                score += 1
                pass_pipe = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()





run = True
while run:

	clock.tick(fps)

	# background
	screen.blit(bg, (0,0))
	# 768 determines the height oft he ground
	screen.blit(ground_img, (ground_scroll, 768))
	#draw pipe and bird
	pipe_group.draw(screen)
	bird_group.draw(screen)
	#bird animation
	bird_group.update()

	#check the score
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pass_pipe == False:
			pass_pipe = True
		if pass_pipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1
				pass_pipe = False
	draw_text(str(score), font, white, int(screen_width / 2), 20)


	#look for collision
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
		game_over = True
	#if bird hit ground the bird die and game ends
	if flappy.rect.bottom >= 768:
		game_over = True
		flying = False

	# if player is not died and continues the game
	if flying == True and game_over == False:
		#generate new pipes for bird to fly througth
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > pipe_frequency:
			pipe_height = random.randint(-100, 100)
			#determine the position of bottom pipe and upper pipe
			btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
			top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe = time_now
		#pipe moving animation
		pipe_group.update()
		#ground and pipe moves while bird is still in the initial position
		ground_scroll -= scroll_speed
		if abs(ground_scroll) > 35:
			ground_scroll = 0
	

	#check for game over and reset
	if game_over == True:
		if button.draw():
			game_over = False
			score = reset_game()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			#when click mouse, game begin and bird start to going downward due to graviry
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()

pygame.quit()
