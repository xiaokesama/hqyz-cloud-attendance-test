from DrissionPage import ChromiumPage, ChromiumOptions
import DrissionPage._elements.none_element
import re
from common import logger, loc
from datetime import datetime
import settings
from common.read_xls import ReadXlsx
import pyautogui
from time import sleep


def re_get_chs(str):
    return re.sub(r'[^\u4e00-\u9fa5]', '', str)


class MyAssert:
    @staticmethod
    def assertEqual(*args):
        logger.info("执行断言")
        for i in range(0,len(args)-1,2):
            logger.info(f"{args[i]} == {args[i+1]}")
            assert args[i] == args[i+1], f"{args[i]} != {args[i+1]}"

    @staticmethod
    def assertNotEqual(*args):
        for i in range(0,len(args)-1,2):
            assert args[i] != args[i+1], f"{args[i]} == {args[i+1]}"

    @staticmethod
    def assertTrue(a):
        assert True

    @staticmethod
    def assertFalse(a):
        assert False

    @staticmethod
    def assertIn(*args):
        for i in range(0,len(args)-1,2):
            assert args[i] in args[i+1], f"{args[i]} not in {args[i+1]}"

    @staticmethod
    def assertNotIn(*args):
        for i in range(0,len(args)-1,2):
            assert args[i] not in args[i+1], f"{args[i]} in {args[i+1]}"

    @staticmethod
    def assertIsNone(*args):
        for i in range(0, len(args)):
            assert args[i] is None or args[i] == "none", f"{args[i]} is not None"

    @staticmethod
    def assertIsNotNone(*args):
        for i in range(0, len(args)):
            assert args[i] is not None and args[i] != "none", f"{args[i]} is None"


class Page(ChromiumPage):

    def my_get_deleted_ele(self,l):
        try:
            element = self.ele(l)
            if isinstance(element, DrissionPage._elements.none_element.NoneElement):
                logger.error("元素{}已删除".format(l))
                return "none"
            logger.error("找到已被删除元素,删除失败")
            return element
        except Exception as e:
            logger.error("元素{}已删除".format(l))
            return "none"

    # 获取元素属性
    def my_get_ele_attr(self, *args):
        try:
            args = list(args)
            element = self.ele(args[0])
            attr = element.attr(args[1])
            logger.error("元素{}的属性{}为：{}".format(args[0], args[1], attr))
        except Exception as e:
            logger.error("元素{}的属性{}不存在".format(args[0], args[1]))
            raise e
        return attr

    def my_input_ele_str(self, loc, value):
        try:
            self.ele(loc).input(value)
        except Exception as e:
            logger.error("向输入框{}输入{}失败".format(loc, value))
            raise e

    def my_scroll(self, num):
        pyautogui.scroll(num)

    def my_click(self, loc):
        try:
            self.ele(loc).click()
        except Exception as e:
            logger.error("点击元素{}失败".format(loc))
            raise e

    def my_get_page_screenshot(self,id,name):
        # 获取报错时的页面截图，命名规范： 截图时间_xx页面_xx操作
        self.get_screenshot(path=settings.ERROR_SCREENSHOT_PATH,name="{}_{}_{}.png".format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),id,name))

    # 鼠标相对移动一定距离
    def my_move_to(self, *args):
        try:
            self.actions.move_to(args)
        except Exception as e:
            logger.error("鼠标移动到元素{}失败".format(args))

    # 通过按钮上传文件
    def my_upload_file(self, *args):
        try:
            self.ele(*args[0]).click.to_upload(r'{}'.format(args[1]))
        except Exception as e:
            logger.error("通过元素{}上传文件{}失败".format(args[0], args[1]))
            raise e

    def my_click(self,loc):
        self.ele(loc).click()


class ActionExecutor(MyAssert):

    def __init__(self, page):
        self.page = page

    # 解析参数
    def parse_param(self, input_params):
        result = re.split('[;]', input_params)
        logger.info("解析参数：{}".format(result))
        for i in range(len(result)):
            # 解析参数："设备管理.区域管理" => xpath://*[@id="su"]
            if i == 0 and len(re_get_chs(result[i])) >= len(result[i]) * 0.5 and '{' not in result[i] and '}' not in result[i]:
                result[i] = loc.get_ele(result[i].replace("loc:", ""))
            if result[i][0] == '{' and result[i][-1] == '}':
                result[i] = getattr(self, result[i][1:-1])
        logger.info("解析结果：{}".format(result))
        return result

    def execute(self, test_case: dict) -> None:
        logger.info("=========={}号用例：{}测试开始==========".format(test_case['id'], test_case['name']))
        actions = test_case["actions"]
        for action in actions:
            # 解析参数
            try:
                input_param = self.parse_param(action['input_param'])
            except Exception as e:
                logger.error("参数解析出错")
                raise e
            # 断言
            try:
                if "assert" in action['keyword']:
                    logger.info("执行断言{}，参数为{}".format(action['keyword'],input_param))
                    getattr(self, action['keyword'])(*input_param)
                    sleep(1)
                    continue
            except Exception as e:
                logger.error("断言执行出错")
                raise e
            # 执行动作
            try:
                # 判断self.page有没有该方法，如果没有就调用self.page.actions对象
                myaction = self.page if hasattr(self.page, action['keyword']) else self.page.actions
                # 根据有没有返回值来判断使用setattr还是使用setattr
                if action['output_param'] is None:
                    logger.info("执行{}动作，输入参数为{}".format(action['keyword'], input_param))
                    getattr(myaction, action['keyword'])(*input_param)
                    sleep(1)
                else:
                    logger.info("执行{}动作，输入参数为{},设置参数{}".format(action['keyword'], input_param, action['output_param']))
                    setattr(self, action['output_param'], getattr(myaction, action['keyword'])(*input_param))
                    sleep(1)
            except Exception as e:
                logger.error("执行{}动作出错,进行了截图，名称为：{}_{}.png".format(action['keyword'],test_case['id'], test_case['name']))
                # 暂时关闭了截图，因为必须要窗口在最前面
                try:
                    self.page.get_screenshot(test_case['id'], test_case['name'])
                except Exception as e2:
                    logger.error("截图出错")
                    raise e2
                raise e
        logger.info("=========={}号用例：{}测试结束==========".format(test_case['id'], test_case['name']))


if __name__ == '__main__':
    # 连接浏览器
    co = ChromiumOptions()
    co.ignore_certificate_errors()
    co.set_address("127.0.0.1:9999")
    page = Page(addr_or_opts=co)

    # 新建执行器
    ae = ActionExecutor(page)

    # 读取用例
    cases = ReadXlsx(settings.CASE_TABLE).read_cases("单个")

    # 执行用例
    ae.execute(cases[0])

