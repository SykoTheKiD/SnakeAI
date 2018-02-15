import snake_detection as sd
from PIL import ImageGrab
from math import sqrt
import numpy as np
import imutils
import cv2

while True:
	screen_image = ImageGrab.grab(bbox=(13, 80, 950, 1030))
	screen = np.array(screen_image)
	screen = sd.detect_snake_head(screen)

	gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	if len(cnts) == 2:
		p1, p2 = sd.get_square_center(cnts[0]), sd.get_square_center(cnts[1])
		if sd.collinear(p1, p2):
			cv2.line(screen, p1, p2, (0, 255, 0), 10)

	cv2.imshow("Vue", screen)

	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break