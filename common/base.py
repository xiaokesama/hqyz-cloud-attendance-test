from playwright.sync_api import Page, Locator, expect


# 1.改造这里位drissionpage
# 2. 自定义用例读取xlsx,然后自定义用力排序规则，某几个模块的用例优先加载，表格优先级标注一下，表格内部用例优先级用名称排序
# 3. 加日志，加截图，加报告
# 4. 参考po2,po3修改框架结构
# po模式，逻辑和对象都写到表格里面，分表格写：逻辑一个，对象一个，用下拉列表选择

class ActionExecutor:
    def __init__(self, page: Page):
        self.page = page

    def execute(self, actions:[]) -> None:
        """执行一系列操作"""
        action_map = {
            "跳转": lambda act: self.page.goto(act["网址"]),
            "单击": lambda act: self.page.click(act["选择器"], button="left"),
            "右键单击": lambda act: self.page.click(act["选择器"], button="right"),
            "双击": lambda act: self.page.dblclick(act["选择器"]),
            "输入": lambda act: self.page.fill(act["选择器"], act["值"]),
            "按键": lambda act: self.page.press(act["选择器"], act["按键"]),
            "勾选": lambda act: self.page.check(act["选择器"]),
            "取消勾选": lambda act: self.page.uncheck(act["选择器"]),
            "悬停": lambda act: self.page.hover(act["选择器"]),
            "聚焦": lambda act: self.page.focus(act["选择器"]),
            "清除输入内容": lambda act: self.page.locator(act["选择器"]).clear(),
            "获取元素内部HTML": lambda act: self.page.inner_html(act["选择器"]),
            "获取元素数量": lambda act: self.page.locator(act["选择器"]).count(),
            "获取元素文本内容": lambda act: self.page.inner_text(act["选择器"]),
            "获取元素属性值": lambda act: self.page.get_attribute(act["选择器"], act["属性名"]),
            "获取元素列表的文本内容": lambda act: self.page.locator(act["选择器"]).all_inner_texts(),
            "拖拽": lambda act: self.page.drag_and_drop(act["源"], act["目标"]),
            "滚动元素至可见": lambda act: self.page.locator(act["选择器"]).scroll_into_view_if_needed(),
            "等待URL": lambda act: self.page.wait_for_url(act["网址"]),
            "等待超时": lambda act: self.page.wait_for_timeout(act["超时时间"]),
            "等待加载状态": lambda act: self.page.wait_for_load_state(act["状态"]),
            "等待元素状态": lambda act: self.page.wait_for_selector(act["选择器"]).wait_for_element_state(act["状态"]),
            "断言(元素可见)": lambda act: expect(self.page.locator(act["选择器"])).to_be_visible(),
            "断言(元素不可见)": lambda act: expect(self.page.locator(act["选择器"])).to_be_hidden(),
            "断言(元素包含文本内容)": lambda act: expect(self.page.locator(act["选择器"])).to_contain_text(act["预期文本"]),
            "断言(元素具有DOM属性)": lambda act: expect(self.page.locator(act["选择器"])).to_have_attribute(act["属性名"], act["属性值"]),
        }
        for action in actions:
            action_type = action["操作类型"]
            if action_type in action_map:
                action_map[action_type](action)
                print(f"[操作]: {action}")
            else:
                print(f"无效的操作类型: {action_type}")
