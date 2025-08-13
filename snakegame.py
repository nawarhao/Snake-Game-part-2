import pygame
import random

pygame.init()
cell_size = 20
cols, rows = 40, 30
screen_width, screen_height = cols * cell_size, rows * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

APPLE_COUNT = 5

class Snake:
    def __init__(self):
        self.body = [(10, 10)]
        self.direction = (1, 0)
        self.grow = False
    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        if (new_head in self.body or
            new_head[0] < 0 or new_head[0] >= cols or
            new_head[1] < 0 or new_head[1] >= rows):
            return False
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True
    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir
    def draw(self):
        snake_color = (59, 113, 159)       # original blue
        outline_color = (30, 60, 90)       # darker blue for outline

        for x, y in self.body:
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            # Draw outline (slightly bigger rect behind)
            outline_rect = rect.inflate(2, 2)
            pygame.draw.rect(screen, outline_color, outline_rect)
            # Draw main snake block
            pygame.draw.rect(screen, snake_color, rect)

class Apple:
    def __init__(self, snake_body):
        self.respawn(snake_body)
    def respawn(self, snake_body):
        while True:
            new_pos = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            if new_pos not in snake_body:
                self.pos = new_pos
                break
    def draw(self):
        apple_color = (255, 0, 0)
        outline_color = (150, 0, 0)   # dark red outline

        rect = pygame.Rect(self.pos[0] * cell_size, self.pos[1] * cell_size, cell_size, cell_size)
        outline_rect = rect.inflate(2, 2)
        pygame.draw.rect(screen, outline_color, outline_rect)
        pygame.draw.rect(screen, apple_color, rect)

def spawn_apples(count, snake_body):
    apples = []
    for _ in range(count):
        apples.append(Apple(snake_body))
    return apples

def draw_checkerboard():
    # Softer baby green vibes, easier on the eyes
    light_green = (200, 230, 200)   # pastel mint
    dark_green = (170, 210, 170)    # muted soft green

    for y in range(rows):
        for x in range(cols):
            color = dark_green if (x + y) % 2 == 0 else light_green
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

def draw_text_with_outline(text, font, text_color, outline_color, pos):
    base = font.render(text, True, text_color)
    outline = font.render(text, True, outline_color)

    x, y = pos
    # Draw outline in 8 directions for subtle outline
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
        screen.blit(outline, (x+dx, y+dy))
    screen.blit(base, pos)

snake = Snake()
apples = spawn_apples(APPLE_COUNT, snake.body)
score = 0
font = pygame.font.Font(None, 36)
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_UP]:
            snake.change_direction((0, -1))
        if keys[pygame.K_DOWN]:
            snake.change_direction((0, 1))
        if keys[pygame.K_LEFT]:
            snake.change_direction((-1, 0))
        if keys[pygame.K_RIGHT]:
            snake.change_direction((1, 0))

        if not snake.move():
            game_over = True

        eaten = []
        for apple in apples:
            if snake.body[0] == apple.pos:
                score += 1
                snake.grow = True
                eaten.append(apple)
        for e in eaten:
            apples.remove(e)

        if not apples:
            apples = spawn_apples(APPLE_COUNT, snake.body)

    draw_checkerboard()
    snake.draw()
    for apple in apples:
        apple.draw()

    draw_text_with_outline(f"Score: {score}", font, (255, 255, 255), (0, 0, 0), (10, 10))

    if game_over:
        draw_text_with_outline("GAME OVER", font, (255, 50, 50), (80, 0, 0),
                               (screen_width // 2 - 100, screen_height // 2 - 20))

    pygame.display.flip()
    clock.tick(10)
