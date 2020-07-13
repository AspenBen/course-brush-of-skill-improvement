import pyautogui
import threading
import time
from selenium import webdriver
import re
import pdb
import user_pwd

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 2.5
event=threading.Event()

class Auto_learn:
    def __init__(self):
        self.user = user_pwd.USERNAME
        self.password = user_pwd.PASSWORD
        self.button="button1.png"
        self.x, self.y = pyautogui.position()

    def StartChrome(self):
        option = webdriver.ChromeOptions()
        # run with top authority
        option.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=option)

    def Login(self):
        print("start chrome to login.")
        chrome.get('https://www.bjjnts.cn/login')
        time.sleep(2)
        print("input username&password")
        chrome.find_element_by_name("username").send_keys(self.user)
        chrome.find_element_by_name("password").send_keys(self.password)

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

    def play_last(driver,video_index):
        elements = []
        while True:
            try:
                elements = driver.find_elements_by_css_selector("a[class^='change_chapter lesson-']")
            except:
                print "wait for getting change_chapter"
                pass
            if len(elements):
                print "get change_chapter"
                break

        if video_index+1 > len(elements):
            print "play complate"
        exit(1)

        index = 0
        if video_index == 0:
            for element in elements:
                ProgressBar = re.findall(r"\d+\.?\d*%", element.text)
                if len(ProgressBar):
                    if ProgressBar[0] != '100%':
                        print "0=========="
                        print "ProgressBar: %s" %(ProgressBar[0])
                        print "playing: %d"%(index)
                        print "0=========="
                        element.click()
                        speed_keep(driver,element)
                        return index
                index += 1
        else:
            print "1=========="
            print "playing index: %d"%(video_index)
            print "1=========="
            elements[video_index].click()
            speed_keep(driver,elements[video_index])
            return video_index
    def wait_for_next_play(driver, i):
        while True:
            pause_check(driver)
            flag = 0
            flag = face_cheack(chrome)
            print "flag %s" %(flag)
            if flag == 1:
            driver.refresh()
            i -= 1
            currnt_index = i + 1
            next_index = currnt_index + 1
            #pdb.set_trace()
            sel_rule = "a[class^='change_chapter lesson-%d']" %(next_index)
            print "next lesson %d" %(next_index)
            element_temp = driver.find_element_by_css_selector(sel_rule)
            speed_keep(driver,element_temp)
            ProgressBar_temp  = re.findall(r"\d+\.?\d*%",element_temp.text)
            if len(ProgressBar_temp):
                print "ProgressBar_temp:" + ProgressBar_temp[0]     
                if ProgressBar_temp[0] == '0%' or ProgressBar_temp[0] == '100%' or flag == 1:
                    time.sleep(3)
                    break
        i += 1
        return i

auto_learn=Auto_learn()
auto_learn.thread_start()
