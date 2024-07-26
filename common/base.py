from DrissionPage import ChromiumPage, ChromiumOptions
import DrissionPage._elements.none_element
import re
from common import logger, loc
from datetime import datetime
import settings
from common.read_xlsx import ReadXlsx
import pyautogui


class MyAssert:
    @staticmethod
    def assertEqual(*args):
        for i in range(0,len(args)-1,2):
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

    def get_element(self,l):
        try:
            element = self.ele(l)
        except Exception as e:
            logger.error("元素{}不存在".format(l))
            raise e
        return element

    def get_deleted_element(self,l):
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
    def get_ele_attr(self, *args):
        try:
            args = list(args)
            element = self.get_element(args[0])
            attr = element.attr(args[1])
        except Exception as e:
            logger.error("元素{}的属性{}不存在".format(args[0], args[1]))
            raise e
        return attr

    def ele_input(self, loc, value):
        try:
            self.ele(loc).input(value)
        except Exception as e:
            logger.error("向输入框{}输入{}失败".format(loc, value))
            raise e

    def scroll(self, num):
        pyautogui.scroll(num)

    def click(self, loc):
        try:
            self.ele(loc).click()
        except Exception as e:
            logger.error("点击元素{}失败".format(loc))
            raise e

    def get_page_screenshot(self,id,name):
        # 获取报错时的页面截图，命名规范： 截图时间_xx页面_xx操作
        self.get_screenshot(path=settings.ERROR_SCREENSHOT_PATH,name="{}_{}_{}.png".format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),id,name))


class ActionExecutor(MyAssert):

    def __init__(self, page):
        self.page = page

    # 解析参数
    def parse_param(self, input_params):
        result = re.split('[;]', input_params)
        for _ in result:
            # 解析参数："设备管理.区域管理" => xpath://*[@id="su"]
            if result.index(_) == 0 and "loc:"in _:result[result.index(_)] = loc.get_ele(_.replace("loc:",""))
            # 解析参数：{name} => self.name
            if _[0] == '{' and _[-1] == '}':result[result.index(_)] = getattr(self, _[1:-1])
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
            # 断言部分以后写
            try:
                if "assert" in action['keyword']:
                    logger.info("执行断言{}，参数为{}".format(action['keyword'],action['input_param']))
                    getattr(self, *self.parse_param(action['input_param']))
                    continue
            except Exception as e:
                logger.error("断言执行出错")
                raise e
            # 执行动作
            try:
                if action['output_param'] is None:
                    logger.info("执行{}动作，输入参数为{}".format(action['keyword'], input_param))
                    getattr(self.page, action['keyword'])(*input_param)
                else:
                    logger.info("执行{}动作，输入参数为{},设置参数{}".format(action['keyword'], input_param, action['output_param']))
                    setattr(self, action['output_param'], getattr(self.page, action['keyword'])(*input_param))
            except Exception as e:
                logger.error("执行{}动作出错,进行了截图，名称为：{}_{}.png".format(action['keyword'],test_case['id'], test_case['name']))
                # 暂时关闭了截图，因为必须要窗口在最前面
                try:
                    self.page.get_page_screenshot(test_case['id'], test_case['name'])
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
    cases = ReadXlsx(settings.CASE_TABLE).read_case_by_id("001")

    # 执行用例
    ae.execute(cases[0])

