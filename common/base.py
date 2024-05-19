from DrissionPage import ChromiumPage
import re


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
        assert a!= b, f"{a} == {b}"

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

    def execute(self, actions: list) -> None:
        for action in actions:
            # 断言部分以后写
            if action['step'] == '断言':
                MyAssert.assertEqual(*self.parse_param(action['input_param']))
                continue
            # 处理参数传递
            input_param = self.parse_param(action['input_param'])
            # 执行动作
            if action['output_param'] is None:
                getattr(self.page, action['keyword'])(*input_param)
            else:
                setattr(self, action['output_param'], getattr(self.page, action['keyword'])(*input_param))


if __name__ == '__main__':
    pass