from math import sqrt
import numpy as np
import logging
import cv2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def contour_approximation(contours):
	perimeter = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

def get_snake_body_mask(image):
	white = np.uint8([255, 255, 255])
	return cv2.inRange(image, white, white)

def get_snake_head_mask(image):
	# head mask
	green = np.uint8([156, 204, 101])
	return cv2.inRange(image, green, green)

def get_snake_candy_mask(image):
	snack = np.uint8([233, 30, 99])
	return cv2.inRange(image, snack, snack)
	
def combine_mask(mask1, mask2):
	return cv2.bitwise_or(mask1, mask2)

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

def get_square_center(c):
	M = cv2.moments(c)
	try:
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		return cX, cY
	except Exception as e:
		logger.warn("Division by zero, no squares found")
		return 0, 0

def collinear(p1, p2):
	return (p1[0] == p2[0]) or (p1[1] == p2[1])

def point_distance(p1, p2):
	x_delta = p2[0] - p1[0]
	y_delta = p2[1] - p1[1]
	return sqrt((x_delta**2 + y_delta**2))