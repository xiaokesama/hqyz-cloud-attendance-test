from DrissionPage import ChromiumPage
import pyautogui
from time import sleep

page = ChromiumPage('127.0.0.1:9999')
print(page.title)
page.actions.move_to((100,100))