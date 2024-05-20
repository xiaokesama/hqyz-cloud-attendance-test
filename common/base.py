from DrissionPage import ChromiumPage
import re
from common import logger
from datetime import datetime
import settings


# 1.改造这里位drissionpage，传参要注意,就用setget传参，前面保存为self.msg='',后面调用直接传入{msg}
# 2. 自定义用例读取xlsx,然后自定义用力排序规则，某几个模块的用例优先加载，表格优先级标注一下，表格内部用例优先级用名称排序
# 3. 加日志，加截图，加报告
# 4. 参考po2,po3修改框架结构
# po模式，逻辑和对象都写到表格里面，分表格写：逻辑一个，对象一个，用下拉列表选择

# 先完成第一步
# 夹具和前置后置操作再写一下
# 利用表格，写两个简单的用例


class MyAssert:
    @staticmethod
    def assertEqual(a, b):
        assert a == b, f"{a}!= {b}"

    @staticmethod
    def assertNotEqual(a, b):
        assert a != b, f"{a} == {b}"

    @staticmethod
    def assertTrue(a):
        assert a, f"{a} is not True"

    @staticmethod
    def assertFalse(a):
        assert not a, f"{a} is not False"

    @staticmethod
    def assertIn(a, b):
        assert a in b, f"{a} not in {b}"

    @staticmethod
    def assertNotIn(a, b):
        assert a not in b, f"{a} in {b}"

    @staticmethod
    def assertIs(a, b):
        assert a is b, f"{a} is not {b}"

    @staticmethod
    def assertIsNot(a, b):
        assert a is not b, f"{a} is {b}"

    @staticmethod
    def assertIsNone(a):
        assert a is None, f"{a} is not None"

    @staticmethod
    def assertIsNotNone(a):
        assert a is not None, f"{a} is None"

    @staticmethod
    def assertIsInstance(a, b):
        assert isinstance(a, b), f"{a} is not instance of {b}"

    @staticmethod
    def assertNotIsInstance(a, b):
        assert not isinstance(a, b), f"{a} is instance of {b}"


class Page(ChromiumPage):

    def ele_attr(self, loc, value):
        return self.ele(loc).attr(value)

    def ele_input(self, loc, value):
        self.ele(loc).input(value)

    def ele_click(self, loc):
        self.ele(loc).click()

    def get_page_screenshot(self,id,name):
        # 获取报错时的页面截图，命名规范： 截图时间_xx页面_xx操作
        self.get_screenshot(
            path=settings.ERROR_SCREENSHOT_PATH,
            name="{}_{}_{}.png".format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),id,name))


class ActionExecutor(MyAssert):

    def __init__(self, page):
        self.page = page

    # 后期这是要改的，路径替换
    def parse_param(self, input_params):
        result = re.split('[;, ]', input_params)
        for _ in result:
            if _[0] == '{' and _[-1] == '}':
                result[result.index(_)] = getattr(self, _[1:-1])
        return result

    def execute(self, test_case: dict) -> None:
        logger.info("=========={}号用例：{}测试开始==========".format(test_case['id'], test_case['name']))
        actions = test_case["actions"]
        for action in actions:
            # 断言部分以后写
            try:
                if action['step'] == '断言':
                    MyAssert.assertEqual(*self.parse_param(action['input_param']))
                    continue
            except Exception as e:
                logger.error("断言执行出错")
                raise e
            # 处理参数传递
            try:
                input_param = self.parse_param(action['input_param'])
            except Exception as e:
                logger.error("参数解析出错")
                raise e
            # 执行动作
            try:
                if action['output_param'] is None:
                    getattr(self.page, action['keyword'])(*input_param)
                else:
                    setattr(self, action['output_param'], getattr(self.page, action['keyword'])(*input_param))
            except Exception as e:
                logger.error("{}动作执行出错,进行了截图，名称为：{}_{}.png".format(action['keyword'],test_case['id'], test_case['name']))
                # 暂时关闭了截图，因为必须要窗口在最前面
                # self.page.get_page_screenshot(test_case['id'], test_case['name'])
                raise e
        logger.info("=========={}号用例：{}测试结束==========".format(test_case['id'], test_case['name']))


if __name__ == '__main__':
    page = Page()
    page.get_page_screenshot("asdf",'asdf')
