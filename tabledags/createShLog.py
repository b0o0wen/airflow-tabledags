import re
import os
import stat
from util import render
from templates import sh_daily, sh_weekly, sh_weekly7, sh_monthly, sh_monthly30, sh_retention_daily, sh_retention_monthly, sh_retention_monthly30, sh_retention_weekly, sh_retention_weekly7


def create(rootdir, file):
    if re.match('\..*\.(sql)$', file):
        core_name = file.replace('/', '')
        core_name = core_name.split('.')[1]
        rootdir = rootdir
        core_path = rootdir + 'scripts/' + core_name
        sh_path = core_path + '.sh'
        log_path = core_path + '.log'

        if os.path.exists(sh_path):
            # print(core_name + '.sh already exists')
            pass
        else:
            keyword1 = core_name.split('_')[-1]
            keyword2 = core_name.split('_')[-2]
            with open(sh_path, 'w', encoding='utf-8') as f:
                # 解析sql名来选取模板
                if keyword1 == 'weekly' and keyword2 == 'retention':
                    f.write(render.render(sh_retention_weekly.SH_STR, rootdir, core_name))
                elif keyword1 == 'weekly7' and keyword2 == 'retention':
                    f.write(render.render(sh_retention_weekly7.SH_STR, rootdir, core_name))
                elif keyword1 == 'monthly' and keyword2 == 'retention':
                    f.write(render.render(sh_retention_monthly.SH_STR, rootdir, core_name))
                elif keyword1 == 'monthly30' and keyword2 == 'retention':
                    f.write(render.render(sh_retention_monthly30.SH_STR, rootdir, core_name))
                elif keyword1 == 'daily' and keyword2 == 'retention':
                    f.write(render.render(sh_retention_daily.SH_STR, rootdir, core_name))
                elif keyword1 == 'weekly':
                    f.write(render.render(sh_weekly.SH_STR, rootdir, core_name))
                elif keyword1 == 'weekly7':
                    f.write(render.render(sh_weekly7.SH_STR, rootdir, core_name))
                elif keyword1 == 'monthly':
                    f.write(render.render(sh_monthly.SH_STR, rootdir, core_name))
                elif keyword1 == 'monthly30':
                    f.write(render.render(sh_monthly30.SH_STR, rootdir, core_name))
                else:
                    f.write(render.render(sh_daily.SH_STR, rootdir, core_name))

            # 修改sh权限为755
            os.chmod(sh_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            print('    create .sh: ', core_name + '.sh done')

        if os.path.exists(log_path):
            pass
        else:
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write('1')