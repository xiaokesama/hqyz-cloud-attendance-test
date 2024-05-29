from DrissionPage import ChromiumPage
import base64
import pytesseract
from PIL import Image
from io import BytesIO
from time import sleep
from settings import USER_INFO,LOGIN_URL,MAIN_URL


def get_captcha_code(page):
    url = page.ele("xpath://*[@class='user-layout-login ant-form ant-form-horizontal']//img").attr('src')
    binary_data = base64.b64decode(url[22:])
    img = Image.open(BytesIO(binary_data))
    code = pytesseract.image_to_string(img, lang="chi_sim+eng").replace(' ', '')
    return code


def login(page):
    page.get(MAIN_URL)
    sleep(2)
    while "/user/login" in page.url:
        page.get(LOGIN_URL)
        page.ele('xpath://*[@placeholder="请输入帐户名"]').input(USER_INFO['username'])
        page.ele('xpath://*[@placeholder="请输入密码"]').input(USER_INFO['password'])
        page.ele('xpath://*[@placeholder="请输入验证码"]').input(get_captcha_code(page))
        sleep(1)


def get_element(page,l=[]):
    e = page
    for _ in l:
        print(_)
        e = e.ele(_)
    return e


def ele_attr(page,*args):
    args = list(args)
    e = get_element(page,args[:-1])
    return e.attr(args[-1])


if __name__ == '__main__':
    page = ChromiumPage()
    e = get_element(page,['xpath://a[contains(@href,"/member/memberlist")]','xpath:./span'])
    print(e.attr('innerText'))

