import numpy as np
import cv2


def contour_approximation(contours):
	perimeter = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

def detect_snake_head(image):
	# head mask
	green = np.uint8([156, 204, 101])
	head_mask = cv2.inRange(image, green, green)
	return cv2.bitwise_and(image, image, mask=head_mask)

	cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cvts[0] if imutils.is_cv2() else cnts[1]
	print()
	for c in cnts:
		M = cv2.moments(c)
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
		c = c.astype("int")
		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)