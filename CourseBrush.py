import pyautogui
import threading
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
event=threading.Event()

class Auto_learn:
    def __init__(self):
        self.button="button1.png"
        self.x, self.y = pyautogui.position()

    def get_button_position(self):
        print("get button positon")
        while True:
            try:
                print("watch the 'confirm' button")
                self.position = pyautogui.locateOnScreen(self.button, confidence=0.9)
                if self.position is not None:
                    print("we find it")
                    event.set()
            except KeyboardInterrupt:
                print('\nExit.')
            time.sleep(5)

    def MoveToPositonClick(self):
        print("click wait until button appear")
        while True:
            event.wait()
            print("end wait")
            self.curx, self.cury = pyautogui.center(self.position)
            pyautogui.moveTo(self.curx, self.cury, duration=0.25)
            #pyautogui.click()
            pyautogui.click()
            #time.sleep(5)
            event.clear()

    def thread_start(self):
        button_appear=threading.Thread(target=self.get_button_position,)
        button_appear.start()
        click=threading.Thread(target=self.MoveToPositonClick,)
        click.start()

auto_learn=Auto_learn()
auto_learn.thread_start()
