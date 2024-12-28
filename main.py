import pygame as pg
from random import randrange, choice
import math

pg.init()
pg.font.init()

clock = pg.time.Clock()

SIZE = 30
half_size = SIZE / 2
apple_size = 30

DISPLAY_WIDTH = 811
DISPLAY_HEIGHT = 601

x_snake = randrange(SIZE, DISPLAY_WIDTH - SIZE, SIZE) - half_size
y_snake = randrange(SIZE, DISPLAY_HEIGHT - SIZE, SIZE) - half_size

x_apple = randrange(SIZE, DISPLAY_WIDTH - apple_size, SIZE)
y_apple = randrange(SIZE, DISPLAY_HEIGHT - apple_size, SIZE)

x_square, y_square = 0, 0

snake_color = 'green'
apple_color = 'red'

screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pg.display.set_caption('Snake')

apple_image = pg.image.load('apple.png').convert_alpha()
apple_image = pg.transform.scale(apple_image, (27, 27))

sound_1 = pg.mixer.Sound('minecraft_eat.mp3')
sound_2 = pg.mixer.Sound('omnomnom.mp3')

sounds_eat = [
    sound_1,
    sound_2,
]
sound_tail_eat = pg.mixer.Sound('smeshnyie-zvuki-pukanya.mp3')

move_buttons = {
    pg.K_w: (0, -1), pg.K_UP: (0, -1),
    pg.K_s: (0, 1), pg.K_DOWN: (0, 1),
    pg.K_a: (-1, 0), pg.K_LEFT: (-1, 0),
    pg.K_d: (1, 0), pg.K_RIGHT: (1, 0),
}
new_move_option = (0, 0)
old_move_option = (0, 0)

pg.draw.circle(
    screen,
    snake_color,
    (x_snake, y_snake),
    SIZE
)

tail = [[x_snake, y_snake]]
now = False


def create_gradient_background():
    # Создаем пустое изображение для фона
    background = pg.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    for y in range(DISPLAY_HEIGHT):
        color = (
            int(10 + (245 - 10) * (y / DISPLAY_HEIGHT)),  # Красный компонент
            int(30 + (190 - 30) * (y / DISPLAY_HEIGHT)),  # Зеленый компонент
            int(10 + (90 - 10) * (y / DISPLAY_HEIGHT))    # Синий компонент
        )
        pg.draw.line(background, color, (0, y), (DISPLAY_WIDTH, y))
    # Рисуем сетку на фоне
    for x in range(0, DISPLAY_WIDTH, SIZE):
        pg.draw.line(background, 'darkgreen', (x, 0), (x, DISPLAY_HEIGHT), 1)
    for y in range(0, DISPLAY_HEIGHT, SIZE):
        pg.draw.line(background, 'darkgreen', (0, y), (DISPLAY_WIDTH, y), 1)
    return background


score = 0
score_font = pg.font.SysFont('Comic Sans MS', 30)


def your_score(score):
    value = score_font.render(str(score), True, 'WHITE')
    screen.blit(value, [10, 10])


def draw_snake_tongue(x_snake, y_snake, direction):
    # Параметры для настройки положения и углов языка
    tongue_length = 19  # Длина языка
    tongue_width = 3  # Ширина языка
    split_length = 5  # Длина раздвоенных частей языка

    # Начальная позиция для языка - центр головы змеи
    tongue_x = x_snake
    tongue_y = y_snake

    # Направление языка (вычисляется на основе направления движения змеи)
    angle = math.atan2(direction[1], direction[0])  # Вычисляем угол движения змеи

    # Смещение основного языка
    tongue_end_x = tongue_x + tongue_length * math.cos(angle)
    tongue_end_y = tongue_y + tongue_length * math.sin(angle)

    # Угол для раздвоения языка
    split_angle = math.pi / 4  # Угол раздвоения (можно скорректировать)

    # Отрисовываем язык - он будет красным до выхода из головы
    pg.draw.line(screen, 'red', (tongue_x, tongue_y), (tongue_end_x, tongue_end_y), tongue_width)

    # Отрисовываем первую ветвь языка - красную
    pg.draw.line(screen, 'red', (tongue_end_x, tongue_end_y),
                 (tongue_end_x + split_length * math.cos(angle - split_angle),
                  tongue_end_y + split_length * math.sin(angle - split_angle)), tongue_width)

    # Отрисовываем вторую ветвь языка - красную
    pg.draw.line(screen, 'red', (tongue_end_x, tongue_end_y),
                 (tongue_end_x + split_length * math.cos(angle + split_angle),
                  tongue_end_y + split_length * math.sin(angle + split_angle)), tongue_width)


background = create_gradient_background()

run = True

while run:
    for e in pg.event.get():
        if e.type == pg.QUIT or e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            run = False

        if e.type == pg.KEYDOWN:
            if e.key in move_buttons:
                new_move_option = move_buttons[e.key]

    if not (x_snake - half_size) % SIZE and not (y_snake - half_size) % SIZE:
        old_move_option = new_move_option

    if now:
        if len(tail) == 2:
            tail.append([x_square - half_size, y_square - half_size, SIZE - 6, SIZE - 6])
        tail.append([x_square - half_size, y_square - half_size, SIZE - 6, SIZE - 6])
        now = False

    for i in range(len(tail) - 1):
        if i == 0:
            tail[i + 1][0] = tail[i][0] - 11
            tail[i + 1][1] = tail[i][1] - 11
        else:
            tail[-i][0] = tail[-(i + 1)][0]
            tail[-i][1] = tail[-(i + 1)][1]

    # Сожрал яблоко
    if (x_snake - half_size, y_snake - half_size) == (x_apple, y_apple):
        score += 1
        choice(sounds_eat).play()
        now = True

        if len(tail) == 1:
            x_square = x_snake
            y_square = y_snake
        else:
            x_square = tail[-1][0]
            y_square = tail[-1][1]
            print('Added')

        x_apple = randrange(SIZE, DISPLAY_WIDTH - apple_size, SIZE)
        y_apple = randrange(SIZE, DISPLAY_HEIGHT - apple_size, SIZE)

    if x_snake > DISPLAY_WIDTH:
        x_snake = x_snake - int(DISPLAY_WIDTH / 10) * 10
    elif x_snake < 0:
        x_snake = x_snake + int(DISPLAY_WIDTH / 10) * 10
    elif y_snake > DISPLAY_HEIGHT:
        y_snake = y_snake - int(DISPLAY_HEIGHT / 10) * 10
    elif y_snake < 0:
        y_snake = y_snake + int(DISPLAY_HEIGHT / 10) * 10

    for i in range(3, len(tail)):
        if tail[0] == [tail[i][0] + 11, tail[i][1] + 11]:
            del tail[i:]
            score = 2
            sound_tail_eat.play()
            print('shhh')
            break

    for nothing in range(SIZE):
        screen.blit(background, (0, 0))
        draw_snake_tongue(x_snake, y_snake, old_move_option)
        your_score(score)

        x_snake += old_move_option[0] / 4
        y_snake += old_move_option[1] / 4

        screen.blit(apple_image, (x_apple, y_apple))

        pg.draw.circle(
            screen,
            snake_color,
            (x_snake, y_snake),
            int(SIZE / 2)
        )

        for i in tail[1:]:
            pg.draw.rect(
                screen,
                snake_color,
                tuple(i)
            )

    tail[0] = [x_snake, y_snake]

    clock.tick(40)
    pg.display.flip()

pg.quit()
