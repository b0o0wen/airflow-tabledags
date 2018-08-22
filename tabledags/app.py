import os
import re
from util import list_files, render
from templates.mainpy import HEAD, DAG, SUBDAG
import createShLog
import createSubdag
import parseSql
import psycopg2 as pg

class App(object):
    def __init__(self, rootdir='/Users/xmly/airflow/dags/himalaya/'):
        self.rootdir = rootdir
        self.mainpy = self.rootdir.split('/')[-2]
        os.chdir(self.rootdir+'scripts/')
        pwd = os.getcwd()
        print('# init #  current path: ',pwd)

        self.files = list_files.list_all_files('./')
        self.sql_files = list_files.list_sql_files('./')
        # print(files)
        self.dependence = None

    # 因为create_sh_log create_subdag只需要解析名字，所以入参用相对路径，而establish_dependence要解析内容，所以入参用绝对路径
    def create_sh_log(self):
        print('# create_sh_log #')
        for file in self.sql_files:
            try:
                createShLog.create(self.rootdir, file)
            except Exception as e:
                print('# create_sh_log #  error occurs when createShLog for :', file)
                print(e)
                raise

    def create_subdag(self):
        print('# create_subdag #')
        for file in self.sql_files:
            try:
                createSubdag.create(self.rootdir, file)
            except Exception as e:
                print('# create_subdag #  error occurs when createSubdag for :', file)
                print(e)
                raise

    def establish_dependence(self):
        print('# establish_dependence #')
        conn = pg.connect(dbname="dw", user="bi", password="bi", host="192.168.3.71", port="5432")
        cur = conn.cursor()

        # 删除，再复写，建立依赖
        sql_truncate = 'truncate table dw.tmplayer.hy_table_dependances'
        cur.execute(sql_truncate)
        conn.commit()

        for file in self.sql_files:
            sql_path=self.rootdir+'scripts/'+file.replace('./','')
            to_from_tables = parseSql.parse(sql_path)
            for to_from_table in to_from_tables:
                sql_insert = "insert into dw.tmplayer.hy_table_dependances (to_table,from_table)VALUES ('%s','%s')" % (to_from_table[0],to_from_table[1])
                cur.execute(sql_insert)
                conn.commit()

        sql_process = '''
        SELECT DISTINCT to_table,regexp_split_to_table(from_table, ',') from dw.tmplayer.hy_table_dependances
        where to_table is not null and from_table is not null and to_table <> from_table
        and to_table <>'' and from_table<>'' and to_table not like '%,%' and from_table not like '%d_00_country%';
        '''
        cur.execute(sql_process)
        self.dependence = cur.fetchall()
        cur.close()
        conn.close()

    def rewrite_mainpy(self):
        print('# rewrite_mainpy #')
        # 每次都完全重写mainpy
        with open(self.rootdir+self.mainpy+'.py','w',encoding='utf-8') as f:
            f.write(render.render(HEAD, rootdir=self.rootdir, core_name=''))
        with open(self.rootdir+self.mainpy+'.py','a',encoding='utf-8') as f:
            for file in self.sql_files:
                if re.match('\..*\.(sql)$', file):
                    core_name = file.replace('/', '')
                    core_name = core_name.split('.')[1]
                    if core_name.split('_')[-1] in ('weekly','weekly7','monthly','monthly30'):
                        f.write(render.render(SUBDAG, self.rootdir, core_name))
                    else:
                        f.write(render.render(DAG, self.rootdir, core_name))

        with open(self.rootdir+self.mainpy+'.py','a',encoding='utf-8') as f:
            for dependence in self.dependence:
                f.write(dependence[1]+' >> '+dependence[0]+'\n')




if __name__ == '__main__':
    # rootdir like '/Users/xmly/airflow/dags/himalaya/' 注意结尾的斜杠
    myapp = App(rootdir='/Users/xmly/airflow/dags/himalaya/')
    myapp.create_sh_log()
    myapp.create_subdag()
    myapp.establish_dependence()
    myapp.rewrite_mainpy()
    print('# success! #')