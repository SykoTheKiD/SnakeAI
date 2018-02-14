import snake_detection as sd
from PIL import ImageGrab
import numpy as np
import cv2

while True:
	screen_image = ImageGrab.grab(bbox=(13, 80, 950, 1030))
	screen = np.array(screen_image)
	screen = sd.detect_snake_head(screen)
	cv2.imshow("Vue", cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break