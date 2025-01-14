import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import openpyxl
from settings import CASE_TABLE


# 判断单元格是否为空,判断单元格的值是否为空
def is_not_empty(cell) -> bool:
    if isinstance(cell, str): return cell != ""
    if cell is None:
        return False
    elif isinstance(cell, openpyxl.cell.cell.Cell):
        if cell.value is None or cell.value == "": return False
    return True


def is_empty(cell) -> bool:
    if isinstance(cell, str): return cell == ""
    if cell is None: return True
    if isinstance(cell, openpyxl.cell.cell.Cell):
        if cell.value is None or cell.value == "": return True
    return False


class ReadXlsx:
    def __init__(self, file_path):
        self.file_path = file_path
        self.workbook = openpyxl.load_workbook(file_path, data_only=True)

    # 选择工作表，返回列表
    def select_sheets(self, sheet=None):
        if not sheet: return self.workbook.worksheets
        if sheet in self.workbook.sheetnames: return [self.workbook[sheet]]
        return []

    # 获取所有用例
    def read_cases_from_sheet(self, sheet=None):
        sheets = self.select_sheets(sheet)
        cases = []
        # 遍历表格
        for sheet in sheets:
            case = {}
            # 遍历所有行
            for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                # 跳过空行
                if all(is_empty(cell) for cell in row): continue
                # 开始读取用例id,name
                if is_not_empty(row[0]):
                    # 保存上一个用例
                    if row_num > 2: cases.append(case)
                    # 开始读取新的用例
                    case = {"id": row[0], "name": row[1], "actions": []}
                # 开始读取用例step,keyword,input_param,output_param
                if is_not_empty(row[3]): case["actions"].append(dict(step=row[2], keyword=row[3], input_param=row[4], output_param=row[5]))
            # 保存最后一个用例
            if len(case) > 0: cases.append(case)
        return cases

    # 根据用例id和表名获取用例
    def get_cases(self, case_id = None,sheet = None):
        if sheet is None and case_id is None:return self.read_cases_from_sheet()
        if case_id is None and sheet is not None: return self.read_cases_from_sheet(sheet)
        if case_id is not None and sheet is not None:all_cases = self.read_cases_from_sheet(sheet)
        if case_id is not None and sheet is None:all_cases = self.read_cases_from_sheet()
        results = []
        for case in all_cases:
            if case["id"] in set(str.split(case_id,"&")):
                results.append(case)
        return results


if __name__ == '__main__':
    print(ReadXlsx(CASE_TABLE).get_cases(sheet="执行"))
