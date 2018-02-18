import snake_detection as sd
from random import randint
from game import SnakeGame
from PIL import ImageGrab
import numpy as np
import logging
import imutils
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
		gray = cv2.cvtColor(screen_snake_body, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
		cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
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

		gray = cv2.cvtColor(screen_snake, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
		cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		dist_top, dist_left, dist_right, dist_bottom = -1, -1, -1, -1
		if len(cnts) == 1:
			p1 = sd.get_square_center(cnts[0])
			dist_left = sd.point_distance(p1, (0, p1[1]))
			dist_right = sd.point_distance(p1, (cols, p1[1]))
			dist_top = sd.point_distance(p1, (p1[0], rows))
			dist_bottom = sd.point_distance(p1, (p1[0], 0))

		dist_head_tail = -1
		try:
			dist_head_tail = sd.point_distance(p1, body_center)
		except UnboundLocalError as e:
			logger.error("No snake body found")

		# Get distance between snake head and candy
		full = sd.combine(screen, snake_mask, candy_mask)
		screen_full = full.screen
		gray = cv2.cvtColor(screen_full, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
		cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
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

		cv2.imshow("Vue", screen_snake)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

if __name__ == "__main__":
	main()