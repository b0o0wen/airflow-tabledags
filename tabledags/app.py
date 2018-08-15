import os
import re
from util import listAllFiles, render
from templates.mainpy import HEAD, DAG, SUBDAG
import createShLog
import createSubdag
import parseSql
import psycopg2 as pg

class App(object):
    def __init__(self, rootdir='/Users/xmly/airflow/dags/himalaya/'):
        self.rootdir = rootdir
        os.chdir(self.rootdir+'scripts/')
        pwd = os.getcwd()
        print('# init #  current path: ',pwd)

        self.files = listAllFiles.listAllFiles('./')
        # print(files)
        self.dependence = None

    def create_sh_log(self):
        for file in self.files:
            try:
                createShLog.create(self.rootdir, file)
            except Exception as e:
                print('# create_sh_log #  error occurs when createShLog for :', file)
                print(e)
                raise

    def create_subdag(self):
        for file in self.files:
            try:
                createSubdag.create(self.rootdir, file)
            except Exception as e:
                print('# create_subdag #  error occurs when createSubdag for :', file)
                print(e)
                raise

    def establish_dependence(self):
        conn = pg.connect(dbname="dw", user="bi", password="bi", host="192.168.20.96", port="5432")
        cur = conn.cursor()

        # 删除，再复写，建立依赖
        sql_truncate = 'truncate table dw.jy.hy_table_dependances'
        cur.execute(sql_truncate)
        conn.commit()

        for file in self.files:
            if re.match('\..*\.(sql)$', file):
                filedir=self.rootdir+'scripts/'+file.replace('./','')
                to_from_tables = parseSql.parse(filedir)
                for to_from_table in to_from_tables:
                    sql_insert = "insert into dw.jy.hy_table_dependances (to_table,from_table)VALUES ('%s','%s')" % (to_from_table[0],to_from_table[1])
                    cur.execute(sql_insert)
                    conn.commit()

        sql_process = '''
        SELECT DISTINCT to_table,regexp_split_to_table(from_table, ',') from dw.jy.hy_table_dependances
        where to_table is not null and from_table is not null and to_table <> from_table
        and to_table <>'' and from_table<>'' and to_table not like '%,%' and from_table not like '%d_00_country%';
        '''
        cur.execute(sql_process)
        self.dependence = cur.fetchall()
        cur.close()
        conn.close()

    def rewrite_mainpy(self):
        # 暂时每次都完全重写MainPy
        with open(self.rootdir+'himalaya.py','w',encoding='utf-8') as f:
            f.write(render.render(HEAD, rootdir=self.rootdir, core_name=''))
        with open(self.rootdir+'himalaya.py','a',encoding='utf-8') as f:
            for file in self.files:
                if re.match('\..*\.(sql)$', file):
                    core_name = file.replace('/', '')
                    core_name = core_name.split('.')[1]
                    if core_name.split('_')[-1] in ('weekly','weekly7','monthly','monthly30'):
                        f.write(render.render(SUBDAG, self.rootdir, core_name))
                    else:
                        f.write(render.render(DAG, self.rootdir, core_name))

        with open(self.rootdir+'himalaya.py','a',encoding='utf-8') as f:
            for dependence in self.dependence:
                f.write(dependence[1]+' >> '+dependence[0]+'\n')




if __name__ == '__main__':
    myapp = App('/Users/xmly/airflow/dags/himalaya/')
    myapp.create_sh_log()
    myapp.create_subdag()
    myapp.establish_dependence()
    myapp.rewrite_mainpy()