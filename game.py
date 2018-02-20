import logging

import pyautogui as mv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MOVE_UP = "up"
MOVE_DOWN = "down"
MOVE_LEFT = "left"
MOVE_RIGHT = "right"

MOVES = {0: MOVE_UP, 1: MOVE_DOWN, 2: MOVE_LEFT, 3: MOVE_RIGHT}


class SnakeGame:
    def __init__(self):
        self.score = 0

    @staticmethod
    def move_snake(move_num):
        direction = MOVES[move_num]
        direction = direction.lower()
        if direction == MOVE_UP or direction == MOVE_DOWN or direction == MOVE_LEFT or direction == MOVE_RIGHT:
            mv.keyDown(direction)
            mv.keyUp(direction)
        else:
            logger.error("Invalid Direction Parameter")
            raise Exception("Direction invalid")

    def reset_game(self):
        self.score = 0
        mv.keyDown("space")
        mv.keyUp("space")
