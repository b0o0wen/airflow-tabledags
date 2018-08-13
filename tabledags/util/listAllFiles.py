import os


def listAllFiles(rootdir):
    files = []
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isdir(path):
            files.extend(list_all_files(path))
        if os.path.isfile(path):
            files.append(path)
    return files



if __name__=='__main__':
    os.chdir('/Users/xmly/airflow/dags/himalaya/scripts/')
    x =listAllFiles('./')
    print(x)