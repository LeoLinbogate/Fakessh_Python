import argparse
import os
import sys
from datetime import datetime, timedelta
from format import operate_sql,find_today_files

# 指定要获取文件名的目录
directory = '.'
# 指定要搜索的模式
pattern = 'fakessh-'
today = datetime.now()
# 减去一天
previous_day = (today - timedelta(days=1)).strftime('%Y-%m-%d')

def get_filenames_with_pattern(directory, pattern):
    # 使用 os.listdir() 获取目录中的所有文件名
    filenames = [filename for filename in os.listdir(directory) if pattern in filename]
    return filenames

def scan_import_all():
    # 调用函数并获取文件名列表
    filenames = sorted(get_filenames_with_pattern(directory, pattern))
    # 打印文件名列表
    print(f"All files:{filenames}")
    # 剔除当日
    filename = find_today_files(directory, today.strftime('%Y-%m-%d'))
    if filename:
        print(f"排除日期{filename}")
        filenames.remove(filename)
        print(f"import files:{filenames}")
        operate_sql(filenames)
    else:
        operate_sql(filenames)

def import_lastday():
      if find_today_files(directory,previous_day):
          filename = [find_today_files(directory,previous_day)]
          print(filename)
          operate_sql(filename)
      else:
        print(f"{previous_day} not found")
# def import_spec_day():

def main():
    parser = argparse.ArgumentParser(
        description="Example script that executes different methods based on command-line arguments.")

    # 添加一个命令行参数
    parser.add_argument('-a', type=str, help="Specify the action to perform: 'lastday' or 'scan'")

    # 解析命令行参数
    args = parser.parse_args()

    # 根据命令行参数执行不同的方法
    if args.a == 'lastday':
        import_lastday()
    elif args.a == 'scan':
        scan_import_all()
    else:
        print("Invalid action specified. Use 'lastday' or 'scan'.")

if __name__ == "__main__":
    main()
