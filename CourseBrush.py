import pyautogui
import threading
import time
from selenium import webdriver
import re
import pdb
import user_pwd

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1
event=threading.Event()

class Auto_learn:
    def __init__(self):
        self.user = user_pwd.USERNAME
        self.password = user_pwd.PASSWORD
        self.button="button1.png"
        self.x, self.y = pyautogui.position()
        self.index = 0

    def StartChrome(self):
        options = webdriver.ChromeOptions()
        # run with top authority
        #options.add_argument('--no-sandbox')
        #options.add_argument("--user-data-dir="+r"/home/zhangben/chrome")
        #options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_extension("accelerate.crx")
        self.driver = webdriver.Chrome(chrome_options=options)
        #self.driver = webdriver.Chrome()

    def KeepSpeed(self, index):
        while True:
            print("sleep 30s to watch speed every time")
            time.sleep(30)
            try:
                speed_element = self.driver.find_element_by_css_selector('.tc-videoController')
                speed_str = re.findall(r"\d+\.?\d*",speed_element.text)
            except:
                speed_str = 'unknow'
                print("the speed can not get now")
                continue

            if speed_str is not 'unknow':
                speed = float(speed_str[0])

            if speed < 4:
                print("the speed of current video is {}, accelerate to 4 times speed to play".format(speed))
                accelerate_time = 4.0 - speed
                for i in range(int(accelerate_time * 10)):
                    self.videos[index].send_keys('D')
            else:
                print("currently, the video is keeping play with 4 times speed")

    def Login(self):
        print ("start chrome to login.")
        self.StartChrome()
        self.driver.get("https://www.bjjnts.cn/login")
        time.sleep(2)
        print("input username&password")
        self.driver.find_element_by_name("username").send_keys(self.user)
        self.driver.find_element_by_name("password").send_keys(self.password)
        self.driver.find_element_by_class_name("login_btn").click()
        print("login successfully")

    def GetAllVedio(self):
        print("watch ACCA F7 Finance Report")
        self.driver.get("https://www.bjjnts.cn/lessonStudy/5/90")
        self.videos = self.driver.find_elements_by_css_selector("a[class^='change_chapter lesson-']")
        #try play first video
        #elements[self.index].click()
        return

    def FindButtonToClick(self):
        print("Find button positon and click")
        while True:
            try:
                print("watch the 'confirm' button every 10 senconds")
                self.position = pyautogui.locateOnScreen(self.button, confidence=0.9)
                if self.position is not None:
                    print("we find it")
                    self.curx, self.cury = pyautogui.center(self.position)
                    pyautogui.moveTo(self.curx, self.cury, duration=0.25)
                    #pyautogui.click()
                    pyautogui.click()
                    
            except KeyboardInterrupt:
                print('\nExit.')
            time.sleep(10)

    def CheckProgress(self, index):
        sel_rule = "a[class^='change_chapter lesson-%d']"%(index+1)
        element_temp = self.driver.find_element_by_css_selector(sel_rule)
        try:
            Progress = re.findall(r"\d+\.?\d*%",element_temp.text)
            current_progress = Progress[0]
        except:
            print("the lesson are locked")
            current_progress = 'lock'
        return current_progress

    def PlayVedio(self):
        self.GetAllVedio()
        self.videos[self.index].click()
        while self.index < len(self.videos):
            time.sleep(30)
            current_video_progress = self.CheckProgress(self.index)
            next_video_progress = self.CheckProgress(self.index + 1)
            print(current_video_progress)
            print(next_video_progress)
            if current_video_progress == '100%' and next_video_progress != 'lock':
                print("play next video")
                try:
                    self.index = self.index + 1
                    self.videos[self.index].click()
                except:
                    print("ignore this time")
            else:
                print("keep watch this vedio until it finished")

    def StartCourseLesson(self):
        watch_button = threading.Thread(target=self.FindButtonToClick,)
        play_next_lesson = threading.Thread(target=self.PlayVedio,)
        keep_speed = threading.Thread(target=self.KeepSpeed,args=(self.index,))
        watch_button.start()
        play_next_lesson.start()
        keep_speed.start()

auto_learn=Auto_learn()
#auto_learn.thread_start()
auto_learn.Login()
time.sleep(5)
auto_learn.StartCourseLesson()
