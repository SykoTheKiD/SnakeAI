import numpy as np
import cv2

def detect_snake_head(image):
	# head mask
	green = np.uint8([156, 204, 101])
	head_mask = cv2.inRange(image, green, green)
	return cv2.bitwise_and(image, image, mask=head_mask)