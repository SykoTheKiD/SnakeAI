import snake_detection as sd
from random import randint
from PIL import ImageGrab
import numpy as np
import imutils
import cv2

def main():
	while True:
		screen_image = ImageGrab.grab(bbox=(13, 80, 960, 1050))
		screen = np.array(screen_image)
		snake_mask = sd.get_snake_head_mask(screen)
		candy_mask = sd.get_snake_candy_mask(screen)
		full_mask = sd.combine_mask(snake_mask, candy_mask)

		screen_snake = cv2.bitwise_and(screen, screen, mask=snake_mask)
		screen_full = cv2.bitwise_and(screen, screen, mask=full_mask)

		rows = screen.shape[0]
		cols = screen.shape[1]

		gray = cv2.cvtColor(screen_snake, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
		cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		if len(cnts) == 1:
			p1 = sd.get_square_center(cnts[0])
			dist_left = sd.point_distance(p1, (0, p1[1]))
			dist_right = sd.point_distance(p1, (cols, p1[1]))
			dist_top = sd.point_distance(p1, (p1[0], rows))
			dist_bottom = sd.point_distance(p1, (p1[0], 0))
			# cv2.line(screen_snake, p1, (0, p1[1]), (0, 255, 0), 10)
			# cv2.line(screen_snake, p1, (p1[0], 0), (0, 255, 0), 10)
			# cv2.line(screen_snake, p1, (cols, p1[1]), (0, 255, 0), 10)
			# cv2.line(screen_snake, p1, (p1[0], rows), (0, 255, 0), 10)

		gray = cv2.cvtColor(screen_full, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
		cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]
		if len(cnts) == 2:
			p1, p2 = sd.get_square_center(cnts[0]), sd.get_square_center(cnts[1])
			if sd.collinear(p1, p2):
				dist_candy = sd.point_distance(p1, p2)
				# cv2.line(screen_full, p1, p2, (255, 255, 0), 10)

		# cv2.imshow("Vue", screen_snake)

		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

if __name__ == "__main__":
	main()