import os
import re


def list_all_files(rootdir):
    files = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isdir(path):
            files.extend(list_all_files(path))
        if os.path.isfile(path):
            files.append(path)
    return files


def list_sql_files(rootdir):
    files = list_all_files(rootdir)
    sql_files = []
    for file in files:
        if re.match('.*\.(sql)$', file):
            sql_files.append(file)
    return sql_files


if __name__ == '__main__':
    os.chdir('/Users/xmly/airflow/dags/himalaya/')
    x = list_all_files('./')
    y = list_sql_files('./')
    print(x[0])
    print(x)
    print(y)
