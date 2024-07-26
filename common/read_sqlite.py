import sqlite3
import pandas as pd
import settings


# 递归获取目标xpath  设备管理.区域管理
def get_ele(data, names):
    parent_id = 1
    names = names.split('.')
    while len(names) > 0:
        item = [_ for _ in data if _[1] == names[0] and str(_[4]) == str(parent_id)]
        if len(item) == 0:
            print("元素不存在")
            return None
        if len(names) == 1:
            return item[0][2]
        else:
            names = names[1:]
            parent_id = item[0][0]


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

    def insert_data(self, name, ele_loc, note, parent_id):
        self.cursor.execute("INSERT INTO locations (name, ele_loc, note, parent_id) VALUES (?,?,?,?)",
                            (name, ele_loc, note, parent_id))
        self.conn.commit()

    def insert_data_with_id(self, id, name, ele_loc, note, parent_id):
        self.cursor.execute("INSERT INTO locations (id, name, ele_loc, note, parent_id) VALUES (?,?,?,?,?)",
                            (id, name, ele_loc, note, parent_id))
        self.conn.commit()

    def view_data(self):
        self.cursor.execute("SELECT * FROM locations")
        rows = self.cursor.fetchall()
        return rows

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
        names = names.split('.')
        while len(names) > 0:
            item = [_ for _ in self.data if _[1] == names[0] and str(_[4]) == str(parent_id)]
            if len(item) == 0:return None
            if len(names) == 1:
                return item[0][2]
            else:
                names = names[1:]
                parent_id = item[0][0]

    def insert_ele(self, name, ele_loc, note, parent_id):
        # 查询是否有相同的元素，主要判断：name、parent_id
        items = [_ for _ in self.get_data().data if _[1] == name and str(_[4]) == str(parent_id)]
        if len(items) == 0:
            self.insert_data(name, ele_loc, note, parent_id)
            print("元素添加成功")
        else:
            print("元素已存在, 添加失败")

    # 程序结束时会自动调用该方法，释放资源
    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    loc = Location(settings.SQLITE_DB_PATH).get_data()
    loc.insert_ele('区域管理2', 'xpath=//*[@id="region1"]', '区域1', 2)
