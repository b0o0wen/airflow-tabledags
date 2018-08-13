SUBDAG_STR='''from airflow.models import DAG
from airflow.operators import BashOperator
from airflow.operators.python_operator import BranchPythonOperator
import datetime

def should_run():
    wow = datetime.datetime.now().strftime('%d')
    if wow == "01":
        return "run"
    else:
        return "skip"

def {{core_name}}(parent_dag_name, child_dag_name, args):

    dag_subdag = DAG(
        dag_id='%s.%s' % (parent_dag_name, child_dag_name),
        default_args=args,
        schedule_interval='0 1 * * *',
    )

    cond = BranchPythonOperator(
        task_id='condition_weekly',
        python_callable=should_run,
        dag=dag_subdag
    )

    run = BashOperator(
        task_id='run',
        bash_command='sh {{sh_path}} ',
        dag=dag_subdag
    )

    skip = BashOperator(
        task_id='skip',
        bash_command='echo 1 ',
        dag=dag_subdag
    )

    cond >> run
    cond >> skip

    return dag_subdag

'''