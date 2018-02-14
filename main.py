import snake_detection as sd
from PIL import ImageGrab
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
	for c in cnts:
		M = cv2.moments(c)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		c = c.astype("int")
		cv2.drawContours(screen, [c], -1, (0, 255, 0), 2)
	
	cv2.imshow("Vue", screen)
	
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break