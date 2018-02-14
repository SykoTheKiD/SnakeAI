import numpy as np
import cv2


def contour_approximation(contours):
	perimeter = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

def detect_snake_head(image):
	# head mask
	green = np.uint8([156, 204, 101])
	head_mask = cv2.inRange(image, green, green)
	snack = np.uint8([233, 30, 99])
	snack_mask = cv2.inRange(image, snack, snack)
	mask = cv2.bitwise_or(head_mask, snack_mask)
	return cv2.bitwise_and(image, image, mask=mask)

def find_contours(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	for c in cnts:
		M = cv2.moments(c)
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
		c = c.astype("int")
		cv2.drawContours(image, [c], -1, (0, 255, 0), 2)