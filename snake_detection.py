from math import sqrt
import numpy as np
import logging
import imutils
import cv2

SNAKE_BODY = "snake_body"
SNAKE_HEAD = "snake_head"
CANDY = "candy"
GAME_OVER = "game_over"

COLOURS = {SNAKE_BODY: np.uint8([255, 255, 255]), 
		   SNAKE_HEAD: np.uint8([156, 204, 101]), 
		   CANDY: np.uint8([233, 30, 99]),
		   GAME_OVER: np.uint8([255, 0, 0])}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def contour_approximation(contours):
	perimeter = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)

def get_part(image, part):
	try:
		colour = COLOURS[part]
		mask = cv2.inRange(image, colour, colour)
		screen = cv2.bitwise_and(image, image, mask=mask)
		return Screen(mask, screen)
	except KeyError as e:
		logger.error("Invalid Part")

	
def combine(image, mask1, mask2):
	mask = cv2.bitwise_or(mask1, mask2)
	screen = cv2.bitwise_and(image, image, mask=mask)
	return Screen(mask, screen)

def find_contours(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]
	cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	return cnts

def get_contour_props(c):
	M = cv2.moments(c)
	area = M["m00"]
	cX, cY = 0, 0
	try:
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
	except Exception as e:
		logger.warn("Division by zero, no squares found")
	return Contour((cX, cY), area)

def collinear(p1, p2):
	return (p1[0] == p2[0]) or (p1[1] == p2[1])

def point_distance(p1, p2):
	x_delta = p2[0] - p1[0]
	y_delta = p2[1] - p1[1]
	return sqrt((x_delta**2 + y_delta**2))

def game_over(image):
	screen_game_over = get_part(image, GAME_OVER)
	return cv2.countNonZero(screen_game_over.mask) > 0

class Screen:
	def __init__(self, mask, screen):
		self.mask = mask
		self.screen = screen

class Contour:
	def __init__(self, center, area):
		self.center = center
		self.area = area