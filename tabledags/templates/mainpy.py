HEAD = '''
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators import SubDagOperator

import datetime
import sys

sys.path.append("{{rootdir}}")

DAG_NAME='himalaya'

args = {
    'owner': 'jack',
    'depends_on_past': False,
    'start_date': datetime.datetime(2018, 8, 4),
    'email': ['jack.wei@ximalaya.com'],
    'retries': 3,
    'email_on_retry'：False,
    'retry_delay': datetime.timedelta(minutes=20)
}

dag = DAG(
    dag_id = DAG_NAME,
    default_args=args,
    schedule_interval="0 1 * * *",
)
'''


DAG = '''
{{core_name}} = BashOperator(
    task_id='{{core_name}}',
    bash_command='sh {{sh_path}} ',
    dag=dag
)

'''


SUBDAG = '''
from subdags.{{core_name}} import {{core_name}}
{{core_name}} = SubDagOperator(
    task_id='{{core_name}}',
    subdag={{core_name}}(DAG_NAME, '{{core_name}}', args),
    default_args=args,
    dag=dag,
    trigger_rule='all_done',
)

'''

DEPENDANCE = '''
{{from_table}}>>{{to_table}}

'''