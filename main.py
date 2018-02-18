import snake_detection as sd
from game import SnakeGame
from PIL import ImageGrab
import numpy as np
import logging
import cv2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
	game = SnakeGame()
	while True:
		screen_image = ImageGrab.grab(bbox=(13, 80, 960, 1050))
		screen = np.array(screen_image)

		# Get distance between snake head and snake body
		screen_snake_body = sd.get_part(screen, sd.SNAKE_BODY).screen
		cnts = sd.find_contours(screen_snake_body)
		if len(cnts) == 1:
			M = cv2.moments(cnts[0])
			snake_body_area = M['m00']
			body_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		snake_obj = sd.get_part(screen, sd.SNAKE_HEAD)
		snake_mask = snake_obj.mask
		candy_mask = sd.get_part(screen, sd.CANDY).mask
		screen_snake = snake_obj.screen
		
		# Get distance between snake head and wall
		rows = screen.shape[0]
		cols = screen.shape[1]
		cnts = sd.find_contours(screen_snake)
		dist_top, dist_left, dist_right, dist_bottom, dist_head_tail = -1, -1, -1, -1, -1
		if len(cnts) == 1:
			p1 = sd.get_square_center(cnts[0])
			dist_left = sd.point_distance(p1, (0, p1[1]))
			dist_right = sd.point_distance(p1, (cols, p1[1]))
			dist_top = sd.point_distance(p1, (p1[0], rows))
			dist_bottom = sd.point_distance(p1, (p1[0], 0))

		try:
			dist_head_tail = sd.point_distance(p1, body_center)
		except UnboundLocalError as e:
			logger.error("No snake body found")

		# Get distance between snake head and candy
		full = sd.combine(screen, snake_mask, candy_mask).screen
		cnts = sd.find_contours(full)
		dist_candy = -1
		if len(cnts) == 2:
			p1, p2 = sd.get_square_center(cnts[0]), sd.get_square_center(cnts[1])
			if sd.collinear(p1, p2):
				dist_candy = sd.point_distance(p1, p2)

		input_vector = np.array([
			dist_top, 
			dist_bottom, 
			dist_left, 
			dist_right, 
			dist_head_tail, 
			dist_candy
			])

		cv2.imshow("Vue", screen_snake_body)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

if __name__ == "__main__":
	main()