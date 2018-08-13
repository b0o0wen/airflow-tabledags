from jinja2 import Template


def render(template, rootdir, core_name):
    x = Template(template)
    core_name = core_name
    sql_path = rootdir+'scripts/'+core_name+'.sql'
    sh_path = rootdir+'scripts/'+core_name+'.sh'
    log_path = rootdir+'scripts/'+core_name+'.log'
    subdag_path = rootdir+'subdags/'+core_name+'.py'

    y = x.render(rootdir=rootdir, sql_path=sql_path, sh_path=sh_path, log_path=log_path, subdag_path=subdag_path, core_name=core_name)
    # Template.render 是可以给多余的参数的，即使x里没有{{core_name}}也无妨
    return y