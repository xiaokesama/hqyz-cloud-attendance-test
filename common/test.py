from DrissionPage import ChromiumPage, ChromiumOptions
import DrissionPage._elements.none_element
import re
from common import logger, loc
from datetime import datetime
import settings
from common.read_xlsx import ReadXlsx
import pyautogui


def click(self, loc):
    try:
        self.ele(loc).click()
    except Exception as e:
        logger.error("点击元素{}失败".format(loc))
        raise e


if __name__ == '__main__':
    # 连接浏览器
    co = ChromiumOptions()
    co.ignore_certificate_errors()
    co.set_address("127.0.0.1:9999")
    page = ChromiumPage(addr_or_opts=co)
    # page.ele('xpath://*[@id="form"]/div/div[2]/div[2]/input').click.to_upload(r'D:\data\1.jpg')
    # 设置要上传的文件路径
    # page.set.upload_files(r'D:\data\1.jpg')
    # 点击触发文件选择框按钮
    # page.click('xpath://*[@id="su"]')
    page.ele('xpath://*[@id="su"]').click()