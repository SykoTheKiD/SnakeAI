import snake_detection as sd
from game import SnakeGame
from PIL import ImageGrab
import numpy as np
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
	logger.info("Game starting")
	for i in range(5):
		logger.info(i + 1)
		time.sleep(1)

	snakes = []
	snake = SnakeGame()
	while True:
		dist_top, dist_left, dist_right, dist_bottom, dist_head_tail, dist_candy, snake_body_area = -1, -1, -1, -1, -1, -1, -1
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
		except UnboundLocalError as e:
			logger.error("No snake body found")

		# Get distance between snake head and candy
		full = sd.combine(screen, snake_mask, candy_mask).screen
		cnts = sd.find_contours(full)
		if len(cnts) == 2:
			cnt1_prop = sd.get_contour_props(cnts[0])
			cnt2_prop = sd.get_contour_props(cnts[1])
			head, p2 = cnt1_prop.center, cnt2_prop.center
			if sd.collinear(head, p2):
				dist_candy = sd.point_distance(head, p2)

		input_vector = np.array([dist_top, dist_bottom, dist_left, dist_right, dist_head_tail, dist_candy])
		screen_game_over = sd.get_part(screen, sd.GAME_OVER)
		if sd.game_over(screen):
			snake.score = snake_body_area
			snakes.append(snake)
			snake = SnakeGame()
			snake.reset_game()

if __name__ == "__main__":
	main()