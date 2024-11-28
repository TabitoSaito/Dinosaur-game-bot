from PIL import Image
import pyautogui
import cv2
import numpy as np
import keyboard

CACTUS_RGB = (83, 83, 83)
SCREEN_SIZE = pyautogui.size()
CENTER_H = int(SCREEN_SIZE[1] / 2)
CENTER_V = int(SCREEN_SIZE[0] / 2)
SHOW_VIDEO = False
SHOW_PRINT = True


def low_jump():
    if SHOW_PRINT:
        print("low jump")
    pyautogui.press("space")


def duke():
    if SHOW_PRINT:
        print("duke")
        pyautogui.keyDown("Down")


def stand():
    print("stand")
    pyautogui.keyUp("Down")


class BotVision:
    def __init__(self):
        self.frame = None
        self.frame_array = None
        cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

    def update_frame(self, frame: Image.Image):
        self.frame = np.array(frame)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('Live', self.frame)

    def mark_bot_vision(self, cord: tuple[int, int, int, int], frame: Image.Image = None,) -> Image.Image:
        if frame is not None:
            self.frame = frame
        else:
            self.frame = pyautogui.screenshot()
        self.frame_array = np.array(self.frame)
        self.frame_array[cord[1]:(cord[1] + cord[3]), cord[0]:(cord[0] + cord[2])] = [255, 0, 0]
        new_frame = Image.fromarray(self.frame_array)
        return new_frame


def main():
    test = True
    duked = False
    if SHOW_VIDEO:
        bot_vision = BotVision()
    keyboard.wait("1")
    pyautogui.click(x=CENTER_V, y=CENTER_H)
    print("start")
    while test:
        if cv2.waitKey(1) == ord("q"):
            break
        view_fild = (350, CENTER_H + 150, 100, 5)
        frame = pyautogui.screenshot(region=view_fild)
        colors = frame.getcolors()

        for color in colors:
            if CACTUS_RGB == color[1]:
                print("low")
                low_jump()

        if SHOW_VIDEO:
            vision_frame = bot_vision.mark_bot_vision(view_fild)
            # bot_vision.update_frame(vision_frame)

        view_fild = (200, CENTER_H + 60, 100, 5)
        frame = pyautogui.screenshot(region=view_fild)
        colors = frame.getcolors()
        stand_up = True
        for color in colors:
            if CACTUS_RGB == color[1]:
                duke()
                duked = True
                stand_up = False
        if stand_up and duked:
            duked = False
            stand()

        if SHOW_VIDEO:
            vision_frame = bot_vision.mark_bot_vision(view_fild, vision_frame)
            bot_vision.update_frame(vision_frame)


if __name__ == "__main__":
    main()
