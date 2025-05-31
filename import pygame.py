import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇')

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.grow = False

    def move(self):
        head = self.body[0]
        if self.direction == 'UP':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'DOWN':
            new_head = (head[0], head[1] + 1)
        elif self.direction == 'LEFT':
            new_head = (head[0] - 1, head[1])
        else:  # RIGHT
            new_head = (head[0] + 1, head[1])
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        self.grow = False

    def change_direction(self, new_direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

def generate_food(snake):
    while True:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food not in snake.body:
            return food

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = generate_food(snake)
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')

        if not game_over:
            # 移动蛇
            snake.move()
            head = snake.body[0]

            # 检查是否吃到食物
            if head == food:
                snake.grow = True
                food = generate_food(snake)
                score += 1

            # 检查游戏是否结束
            if (head[0] < 0 or head[0] >= GRID_WIDTH or
                head[1] < 0 or head[1] >= GRID_HEIGHT or
                head in snake.body[1:]):
                game_over = True

            # 绘制游戏画面
            screen.fill(BLACK)
            
            # 绘制食物
            food_rect = pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, RED, food_rect)

            # 绘制蛇
            for segment in snake.body:
                segment_rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, GREEN, segment_rect)

            pygame.display.flip()
            clock.tick(10)  # 控制游戏速度

if __name__ == '__main__':
    main()