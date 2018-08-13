# -*- coding:utf-8 -*-
import re

def parse(file):
    if re.match('\/.*\.(sql)$', file):
        print('parsing ', file, ' to pg')
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

            # 去掉注释，注释中会有太多混淆
            content = re.sub('--.*\n', '', content)

            # 去掉save前的分号 与 中间步骤的分号
            content = re.sub(';\n*save', '0000', content)
            content = re.sub('as [a-zA-Z0-9]+[ |\n]*;', '1111', content)

            to_from_tables=[]

            for section in content.split(';'):
                # 取from join 后的dw表为 from_table
                # 取insert、 save as hive后的dw表为 to_table
                # 单个to_table 多个from_table，sql本身不报错，py就不会错
                from_table = re.findall('[from|join][ |\n]+hy\.([a-zA-Z0-9_]*)[ |\n]*', section)
                to_table1 = re.findall('insert[ |\n]+overwrite[ |\n]+table[ |\n]+hy\.([a-zA-Z0-9_]*)[ |\n]+',
                                       section)
                to_table2 = re.findall('insert[ |\n]+into[ |\n]+hy\.([a-zA-Z0-9_]*)[ |\n]+', section)
                to_table3 = re.findall('as[ |\n]+hive\.`hy\.([a-zA-Z0-9_]*)`', section)
                to_table = to_table1 + to_table2 + to_table3

                from_table = ','.join(from_table)
                to_table = ','.join(to_table)
                to_from_tables.append([to_table, from_table])

        return to_from_tables


if __name__ == '__main__':
    x = parse('/Users/xmly/Desktop/hy_sql/base_play_album.sql')
    print(x)