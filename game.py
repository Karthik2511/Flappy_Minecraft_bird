import pygame
import random

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 70 
PIPE_GAP = 220  
BACKGROUND_SPEED = 2

BIRD_IMG = pygame.image.load('bird.png')
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (BIRD_WIDTH, BIRD_HEIGHT))  

PIPE_IMG = pygame.image.load('pipe.png')
PIPE_IMG = pygame.transform.scale(PIPE_IMG, (PIPE_WIDTH, PIPE_WIDTH * 3))  


BACKGROUND_IMG = pygame.image.load('background.png')
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))  

PAUSE_ICON = pygame.image.load('pause.png')
PAUSE_ICON = pygame.transform.scale(PAUSE_ICON, (40, 40)) 


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Minecraft')

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.gravity = 0.6
        self.lift = -15
        self.velocity = 0

    def show(self):
        screen.blit(BIRD_IMG, (self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y > SCREEN_HEIGHT - BIRD_HEIGHT:
            self.y = SCREEN_HEIGHT - BIRD_HEIGHT
            self.velocity = 0

        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def up(self):
        self.velocity = self.lift 

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.top = random.randint(50, SCREEN_HEIGHT // 2 - PIPE_GAP // 2)
        self.bottom = self.top + PIPE_GAP
        self.speed = 3
        self.passed = False 
    def show(self):
        screen.blit(PIPE_IMG, (self.x, self.top - PIPE_IMG.get_height()))
        screen.blit(PIPE_IMG, (self.x, self.bottom))

    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x < -PIPE_WIDTH

    def hits(self, bird):
        if bird.x + BIRD_WIDTH > self.x and bird.x < self.x + PIPE_WIDTH:
            if bird.y < self.top or bird.y + BIRD_HEIGHT > self.bottom:
                return True
        return False

def draw_button(text, x, y, width, height, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x + (width // 2 - text_surface.get_width() // 2), y + (height // 2 - text_surface.get_height() // 2)))
    
    return False

def main_menu():
    running = True
    while running:
        screen.blit(BACKGROUND_IMG, (0, 0))

        if draw_button('Start', 150, 300, 100, 50, GRAY, DARK_GRAY):
            return 'start'

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def pause_menu():
    paused = True
    while paused:
        screen.fill(WHITE)
        
        if draw_button('Resume', 150, 200, 100, 50, GRAY, DARK_GRAY):
            return 'resume'
        
        if draw_button('Exit', 150, 300, 100, 50, GRAY, DARK_GRAY):
            pygame.quit()
            exit()

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def main():
    bird = Bird()
    pipes = [Pipe()]
    clock = pygame.time.Clock()
    score = 0
    font = pygame.font.Font(None, 36)

    background_x1 = 0
    background_x2 = SCREEN_WIDTH
    paused = False

    running = True
    while running:
        clock.tick(30)

        background_x1 -= BACKGROUND_SPEED
        background_x2 -= BACKGROUND_SPEED

        if background_x1 <= -SCREEN_WIDTH:
            background_x1 = SCREEN_WIDTH

        if background_x2 <= -SCREEN_WIDTH:
            background_x2 = SCREEN_WIDTH

        screen.blit(BACKGROUND_IMG, (background_x1, 0))
        screen.blit(BACKGROUND_IMG, (background_x2, 0))

        screen.blit(PAUSE_ICON, (10, 10))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        if 10 + 40 > mouse[0] > 10 and 10 + 40 > mouse[1] > 10:
            if click[0] == 1:
                paused = True

        while paused:
            if pause_menu() == 'resume':
                paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.up()

        bird.update()
        bird.show()

        if pipes[-1].x < SCREEN_WIDTH // 2:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.show()

            if pipe.hits(bird):
                print(f"Bird hit a pipe at position: x={pipe.x}, top={pipe.top}, bottom={pipe.bottom}")
                running = False 

            if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                pipe.passed = True  
                score += 1  
            if pipe.offscreen():
                pipes.remove(pipe)

        score_surface = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 50))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":

    if main_menu() == 'start':
        main()
