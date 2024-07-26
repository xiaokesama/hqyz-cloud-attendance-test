import concurrent.futures
import mysql.connector
from settings import MYSQL_CONFIG


class MySQLDataFetcher:
    def __init__(self, mysql_config, sql, max_workers=4):
        self.mysql_config = mysql_config
        self.sql = sql
        self.max_workers = max_workers

    def fetch_data(self, offset, limit):
        """
        使用 offset 和 limit 参数从 MySQL 表中获取数据
        """
        with mysql.connector.connect(**self.mysql_config) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(self.sql + " LIMIT %s, %s", (offset, limit))
                return cursor.fetchall()

    def fetch_all_data(self):
        # 创建线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 计算每个线程需要处理的数据量
            total_rows = 10000
            chunk_size = total_rows // self.max_workers

            # 提交任务到线程池
            futures = []
            for offset in range(0, total_rows, chunk_size):
                futures.append(executor.submit(self.fetch_data, offset, chunk_size))

            # 收集所有线程的结果
            all_data = []
            for future in concurrent.futures.as_completed(futures):
                all_data.extend(future.result())

        return all_data


# 使用示例
if __name__ == "__main__":
    sql = "SELECT * FROM hqzy_attendance_xpath"
    fetcher = MySQLDataFetcher(MYSQL_CONFIG, sql)
    all_data = fetcher.fetch_all_data()

    print(f"Total rows fetched: {len(all_data)}")
    print(all_data)