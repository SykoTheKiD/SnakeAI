import numpy as np
from PIL import ImageGrab

import snake_detection as sd
from game import *
import random
from genalgo import GenAlgo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    ga = GenAlgo(100)
    index = 0
    snake = SnakeGame()
    while True:
        dist_bottom, dist_candy, dist_head_tail, \
        dist_left, dist_right, dist_top, screen, snake_body_area = get_snake_params()
        input_vector = np.array([dist_top, dist_bottom, dist_left, dist_right, dist_head_tail, dist_candy])
        current_snake = ga.population[index]
        if sd.game_screen(screen, sd.GAME_PAUSE):
            network_predict = current_snake.network.predict(input_vector)
            snake.unpause()
            snake.move_snake(network_predict)
        elif sd.game_screen(screen, sd.GAME_OVER):
            snake.score = snake_body_area
            current_snake.fitness = snake_body_area
            snake.reset_game()

        if index < len(ga.population) - 1:
            index += 1
        else:
            index = 0
            ga.select()
            ga.crossover()
            ga.mutate()


def gen_data():
    file = open("data/data_small.csv", "w")
    file.write("snake_details, move, score, result\n")
    num_runs = 1000
    for i in range(num_runs):
        logger.info(str(i + 1) + "/" + str(num_runs))
        while True:
            snake = SnakeGame()
            dist_bottom, dist_candy, dist_head_tail, \
                dist_left, dist_right, dist_top, screen, snake_body_area = get_snake_params()
            input_vector = [dist_top, dist_bottom, dist_left, dist_right, dist_head_tail, dist_candy]
            if sd.game_screen(screen, sd.GAME_PAUSE):
                snake.unpause()
            move = random.randint(0, 3)
            snake.move_snake(move)
            if sd.game_screen(screen, sd.GAME_OVER):
                snake.score = snake_body_area
                snake.reset_game()
                file.write(str(input_vector) + "," + str(move) + "," + str(snake.score) + ",0\n")
                break
            else:
                file.write(str(input_vector) + "," + str(move) + "," + str(snake.score) + ",1\n")
        snake.reset_game()
    file.close()


def get_snake_params():
    dist_top, dist_left, dist_right, dist_bottom, dist_head_tail, \
        dist_candy, snake_body_area = -1, -1, -1, -1, -1, -1, -1
    screen_image = ImageGrab.grab(bbox=(13, 80, 960, 1050))
    screen = np.array(screen_image)
    # Get distance between snake head and snake body
    screen_snake_body = sd.get_part(screen, sd.SNAKE_BODY).screen
    cnts = sd.find_contours(screen_snake_body)
    if len(cnts) == 1:
        cnt_prop = sd.get_contour_props(cnts[0])
        snake_body_area = cnt_prop.area
        body_center = cnt_prop.center
    snake_obj = sd.get_part(screen, sd.SNAKE_HEAD)
    snake_mask = snake_obj.mask
    candy_mask = sd.get_part(screen, sd.CANDY).mask
    screen_snake = snake_obj.screen
    # Get distance between snake head and wall
    rows = screen.shape[0]
    cols = screen.shape[1]
    cnts = sd.find_contours(screen_snake)
    if len(cnts) == 1:
        cnt_prop = sd.get_contour_props(cnts[0])
        head = cnt_prop.center
        dist_left = sd.point_distance(head, (0, head[1]))
        dist_right = sd.point_distance(head, (cols, head[1]))
        dist_top = sd.point_distance(head, (head[0], rows))
        dist_bottom = sd.point_distance(head, (head[0], 0))
    try:
        dist_head_tail = sd.point_distance(head, body_center)
    except UnboundLocalError:
        logger.error("No snake body found")
    # Get distance between snake head and candy
    full = sd.combine(screen, snake_mask, candy_mask).screen
    cnts = sd.find_contours(full)
    if len(cnts) == 2:
        cnt1_prop = sd.get_contour_props(cnts[0])
        cnt2_prop = sd.get_contour_props(cnts[1])
        head, p2 = cnt1_prop.center, cnt2_prop.center
        dist_candy = sd.point_distance(head, p2)
    return dist_bottom, dist_candy, dist_head_tail, dist_left, dist_right, dist_top, screen, snake_body_area


if __name__ == "__main__":
    # main()
    gen_data()
