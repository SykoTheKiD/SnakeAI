import logging

import pyautogui as mv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MOVE_UP = "up"
MOVE_DOWN = "down"
MOVE_LEFT = "left"
MOVE_RIGHT = "right"


class SnakeGame:
    def __init__(self):
        self.score = 0

    @staticmethod
    def move_snake(direction):
        direction = direction.lower()
        if direction == MOVE_UP or direction == MOVE_DOWN or direction == MOVE_LEFT or direction == MOVE_RIGHT:
            mv.keyDown(direction)
            mv.keyUp(direction)
        else:
            logger.error("Invalid Direction Parameter")
            raise Exception("Direction invalid")

    @staticmethod
    def reset_game():
        mv.keyDown("space")
        mv.keyUp("space")
