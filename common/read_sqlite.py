import sqlite3
import pandas as pd
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage
import settings
import re

def convert_to_tree(data):
    def build_tree(node, data):
        children = [d for d in data if str(d['parent_id']) == str(node['id'])]
        if children:
            node['children'] = children
            for child in children:
                build_tree(child, data)

    root = [d for d in data if d['parent_id'] is None or d['parent_id'] == '0'][0]

    build_tree(root, data)

    return root


def recursiveSearchRow(loc, row, result):
    if row[4] is None or row[4] == "1":return result
    row = loc.search_row_by_id(row[4])
    result = row[1] + "." + result
    return recursiveSearchRow(loc, row, result)


class Location:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS locations
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            ele_loc TEXT,
                            note TEXT,
                            parent_id TEXT)''')
        self.conn.commit()

    def view_data(self):
        self.cursor.execute("SELECT * FROM locations")
        rows = self.cursor.fetchall()
        return rows

    def insert_data(self, name, ele_loc, note, parent_id):
        self.cursor.execute("INSERT INTO locations (name, ele_loc, note, parent_id) VALUES (?,?,?,?)",
                            (name, ele_loc, note, parent_id))
        self.conn.commit()

    def insert_data_with_id(self, id, name, ele_loc, note, parent_id):
        self.cursor.execute("INSERT INTO locations (id, name, ele_loc, note, parent_id) VALUES (?,?,?,?,?)",
                            (id, name, ele_loc, note, parent_id))
        self.conn.commit()

    def delete_data(self, id):
        self.cursor.execute("DELETE FROM locations WHERE id=?", (id,))
        self.conn.commit()

    def update_data(self, id, name, ele_loc, note, parent_id):
        self.cursor.execute("UPDATE locations SET name=?, ele_loc=?, note=?, parent_id=? WHERE id=?",
                            (name, ele_loc, note, parent_id, id))
        self.conn.commit()

    def search_data(self, name):
        self.cursor.execute("SELECT * FROM locations WHERE name=?", (name,))
        rows = self.cursor.fetchall()
        return rows

    def search_row_by_id(self, id):
        self.cursor.execute("SELECT * FROM locations WHERE id=?", (id,))
        row = self.cursor.fetchone()
        return row

    def search_row_by_name_and_parent_id(self, name, parent_id):
        self.cursor.execute("SELECT * FROM locations WHERE name=? and parent_id=?", (name,parent_id))
        row = self.cursor.fetchone()
        return row

    def tree_data(self):
        self.cursor.execute("SELECT * FROM locations")
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows, columns=[column[0] for column in self.cursor.description])
        # 必须返回待键值对
        data = df.to_dict(orient='records')

        # 转换为树形结构
        root = convert_to_tree(data)

        return root

    def get_data(self):
        self.data = self.view_data()
        return self

    def get_ele(self, names):
        parent_id = 1
        if isinstance(names, str):names = re.split(r'[.\s。-]+', names)
        while len(names) > 0:
            item = [_ for _ in self.data if _[1] == names[0] and str(_[4]) == str(parent_id)]
            if len(item) == 0:return None
            if len(names) == 1:
                return item[0][2]
            else:
                names = names[1:]
                parent_id = item[0][0]

    def get_row(self, names):
        parent_id = 1
        if isinstance(names, str):names = re.split(r'[.\s。-]+', names)
        while len(names) > 0:
            item = [_ for _ in self.data if _[1] == names[0] and str(_[4]) == str(parent_id)]
            if len(item) == 0:return None
            if len(names) == 1:
                return item[0]
            else:
                names = names[1:]
                parent_id = item[0][0]

    def insert_ele(self, name, ele_loc, note, parent_id):
        # 查询是否有相同的元素，主要判断：name、parent_id
        items = [_ for _ in self.get_data().data if _[1] == name and str(_[4]) == str(parent_id)]
        if len(items) == 0:
            self.insert_data(name, ele_loc, note, parent_id)
            print("元素添加成功")
            return True
        else:
            print("元素已存在于数据库, 添加失败")
            return False

    def update_ele(self, name, ele_loc, note, parent_id):
        # 查询是否有相同的元素，主要判断：name、parent_id
        items = [_ for _ in self.get_data().data if _[1] == name and str(_[4]) == str(parent_id)]
        if len(items) > 0:
            print("开始更新")
            self.update_data(items[0][0], name, ele_loc, note, parent_id)
            print("元素更新成功")
            return True

    # 程序结束时会自动调用该方法，释放资源
    def __del__(self):
        self.conn.close()


class LocationManager:
    def __init__(self, ):
        self.loc = Location(settings.SQLITE_DB_PATH)
        self.page = None
    
    def get_page(self, port=9999):
        # 打开浏览器
        co = ChromiumOptions()
        co.ignore_certificate_errors()
        co.set_address("127.0.0.1:" + str(port))
        page = ChromiumPage(addr_or_opts=co)
        page.set.timeouts(5)
        self.page = page
        return self

    def get_parent_id(self, names):
        self.loc.get_data()
        if len(re.split(r'[.\s。-]+', names)) == 1: parent_id = 1
        if len(re.split(r'[.\s。-]+', names)) > 1: parent_id = self.loc.get_row(re.split(r'[.\s。-]+', names)[:-1])[0]
        return parent_id

    def get_all_names(self, name):
        self.loc.get_data()
        rows = self.loc.search_data(name)
        results = ""
        for row in rows:
            result = recursiveSearchRow(self.loc, row, name)
            results += result + "\n"
        return results

    def save_xpath(self, names,xpath,note='',parent_id='') -> str:
        # 刷新数据
        self.loc.get_data()
        self.get_page()

        try:
            # 检验xpath是否有效
            print("于页面中获取xpath成功，获取到的html内容为：{}".format(self.page.ele("xpath:" + xpath).html))
            result = "于页面中获取xpath成功，获取到的html内容为：{}".format(self.page.ele("xpath:" + xpath).html)
        except:
            print("xpath无效，请检查")
            return "xpath无效，请检查"

        name = names if re.split(r'[.\s。-]+', names) == 1 else re.split(r'[.\s。-]+', names)[-1]

        if parent_id == '':parent_id = self.get_parent_id(names)

        if self.loc.insert_ele(name, "xpath:" + xpath, note, parent_id):
            print('元素[{},{},{},{}]添加成功'.format(name, "xpath:" + xpath, note, parent_id))
            result += "\n" + '元素[{},{},{},{}]添加成功'.format(name, "xpath:" + xpath, note, parent_id)
        else:
            print('元素[{},{},{},{}]添加失败'.format(name, "xpath:" + xpath, note, parent_id))
            result += "\n" + '元素[{},{},{},{}]添加失败'.format(name, "xpath:" + xpath, note, parent_id)
        return result

    def validate_xpath(self, names):
        # 刷新数据
        self.loc.get_data()
        if self.loc.get_ele(names):
            print("经检查，元素【{}】存在于数据库中,内容为：{}".format(names, self.loc.get_ele(names)))
            result = "经检查，元素【{}】存在于数据库中,内容为：{}".format(names, self.loc.get_ele(names))
        else:
            print("元素不存在于数据库中")
            result = "元素不存在于数据库中"
        return result

    def update_xpath(self, names, xpath, note='', parent_id=''):
        # 刷新数据
        self.loc.get_data()

        result = ""
        if len(re.split(r'[.\s。-]+', names)) == 0:
            result += "元素路径不能为空"
            return result

        name = names if re.split(r'[.\s。-]+', names) == 1 else re.split(r'[.\s。-]+', names)[-1]

        if parent_id == '':parent_id = self.get_parent_id(names)

        # 保存到数据库
        if self.loc.update_ele(name, "xpath:" + xpath, note, parent_id):
            print('元素[{},{},{},{}]更新成功'.format(name, "xpath:" + xpath, note, parent_id))
            result += "\n" + '元素[{},{},{},{}]更新成功'.format(name, "xpath:" + xpath, note, parent_id)
        else:
            print('元素[{},{},{},{}]更新失败'.format(name, "xpath:" + xpath, note, parent_id))
            result += "\n" + '元素[{},{},{},{}]更新失败'.format(name, "xpath:" + xpath, note, parent_id)
        return result


if __name__ == '__main__':
    name = '设备管理.设备列表.添加设备.取消2'
    xpath = '/html/body/div[3]/div/div[2]/div/div/div[2]/div[2]/button[11]'
    note = ''
    parent_id = ''
    manager = LocationManager()
    # manager.update_xpath(name,xpath,note,parent_id)
    # manager.save_xpath(name,xpath,note,parent_id)
    # manager.validate_xpath(name)
    print(manager.get_all_names('取消'))
