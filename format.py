import os
import pymysql
from datetime import datetime
from dbconfig import  db_config

# 获取今天的日期，格式化为 YYYYMMDD
# today = datetime.now().strftime('%Y-%m-%d')

def find_today_files(directory,day):
    # 遍历指定目录下的所有文件
    found = False
    for file in os.listdir(directory):
        # 检查文件名是否包含今天的日期
        if day in file:
            # found = True
            return os.path.join(directory, file).lstrip('./')
    if not found:
        return found

# def find_file_path(directory):
#     # 找到所有匹配的文件
#     for file_path in find_today_files(directory):
#         todayFile = file_path
#     return  todayFile

def read_file(filename):
            with open(filename,'r',errors='ignore') as file:
                recordsToInsert = []
                records_count = 0
                for line in file:
                    item = line.strip().split()
                    #剔除没有账号密码的数据
                    if len(item) ==6:
                        # 打印分割后的结果，或进行其他处理
                        # print(items)
                        date = item[0].replace("/","-")
                        time = item[1].split(".",1)[0]
                        addr = item[2].split(":",1)[0]
                        client = item[3]
                        username = item[4]
                        paswd = item[5]
                        records_count +=1
                        record = (date,time,addr,client,username,paswd)
                        recordsToInsert.append(record)
                return recordsToInsert,records_count

def insert_his(connection,history):
    try:
        with connection.cursor() as cursor:
            date = history[0]
            count = history[1]
            check_sql = """
                        SELECT COUNT(*)
                        FROM history_log
                        WHERE hdate = %s
                        """
            cursor.execute(check_sql,(date,))
            result = cursor.fetchone()[0]
            if result > 0:
                update_sql = """
                            UPDATE history_log
                            SET hcount = %s
                            WHERE hdate = %s
                            """
                cursor.execute(update_sql,(count,date,))
                print(f"{history[0]} upadte successfully")
            else:
                sql = "INSERT INTO `history_log` (`hdate`, `hcount`) VALUES (%s, %s)"
                cursor.execute(sql,history)
                connection.commit()
                print(f"{history[0]} insert successfully.")
    except Exception as e:
        print(f"Error inserting history: {e}")

def insert_records(connection, records):
    try:
        with connection.cursor() as cursor:
            # SQL 插入语句
            sql1 = "INSERT INTO `records` (`date`, `time`, `addr`, `client`, `username`, `passwd`) VALUES (%s, %s, %s, %s, %s, %s)"

            # 批量执行插入
            cursor.executemany(sql1, records)

            # 提交事务
            connection.commit()

            print(f"{cursor.rowcount} record(s) inserted successfully.")
    except Exception as e:
        print(f"Error inserting records: {e}")

def extract_date_from_filename(filename):
    # 使用 '-' 分割文件名
    parts = filename.split('-')
    # 从分割后的列表中提取日期部分
    date = '-'.join(parts[1:4])
    return date

def operate_sql(files):
    try:
        for file in files:
            recordsToInsert,records_count =read_file(file)
            his_log = (extract_date_from_filename(file),records_count)
            # 建立数据库连接
            connection = pymysql.connect(**db_config)
            # 插入记录
            insert_records(connection, recordsToInsert)
            insert_his(connection,his_log)
    finally:
        # 关闭数据库连接
        if connection:
            connection.close()