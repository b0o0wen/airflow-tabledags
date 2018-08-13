import re
import os
from util import render
from templates import subdag_monthly, subdag_weekly, subdag_weekly7


def create(rootdir, file):
    if re.match('\..*\.(sql)$', file):
        core_name = file.replace('/', '')
        core_name = core_name.split('.')[1]
        py_path = rootdir + 'subdags/' + core_name + '.py'

        if os.path.exists(py_path):
            pass
        else:
            keyword1 = core_name.split('_')[-1]
            # 解析sql名来选取模板，且只有weekly monthly的才需要生成subdag
            if keyword1 == 'weekly':
                with open(py_path, 'w', encoding='utf-8') as f:
                    f.write(render.render(subdag_weekly.SUBDAG_STR, rootdir, core_name))
                # 无需修改.py权限，该with open 默认为644
                print('create subdag: ', core_name + '.py done')
            elif keyword1 == 'weekly7':
                with open(py_path, 'w', encoding='utf-8') as f:
                    f.write(render.render(subdag_weekly7.SUBDAG_STR, rootdir, core_name))
                print('create subdag: ', core_name + '.py done')
            elif keyword1 == 'monthly' or keyword1 == 'monthly30':
                with open(py_path, 'w', encoding='utf-8') as f:
                    f.write(render.render(subdag_monthly.SUBDAG_STR, rootdir, core_name))
                print('create subdag: ', core_name + '.py done')
            else:
                pass
