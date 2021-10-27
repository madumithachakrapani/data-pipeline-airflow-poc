try:
    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
    from airflow.operators.dummy_operator import DummyOperator
    from airflow.operators.email_operator import EmailOperator
    from datetime import datetime
    import pandas as pd
    from task_spotify_data_extract import run_spotify_etl
    from task_stage_data_in_mongo import store_in_mongo
    from task_transform_data import transform_raw_data
    from task_build_report import build_report
    from task_transfer_file import transfer_file_to_drive

    print("All Dag modules are ok ......")
except Exception as e:
    print("Error  {} ".format(e))

def download_data_from_spotify(*args, **context):
    execution_date = context['execution_date']
    run_id = context['dag_run'].run_id
    spotify_raw_extract = run_spotify_etl(run_id, execution_date)
    is_data_available = False
    if(spotify_raw_extract["songs"]):
        is_data_available = True
    context['ti'].xcom_push(key='spotify_raw_extract', value=spotify_raw_extract)
    context['ti'].xcom_push(key='is_data_available', value=is_data_available)

def is_data_available(*args, **context):
    is_data_present = context.get("ti").xcom_pull(key="is_data_available")
    return 'stage_raw_data_in_mongo' if is_data_present else 'no_data_available'

def stage_raw_data_in_mongo(*args, **context):
    spotify_raw_extract = context.get("ti").xcom_pull(key="spotify_raw_extract")
    store_in_mongo(spotify_raw_extract)

def transform_data(*args, **context):
    spotify_raw_extract = context.get("ti").xcom_pull(key="spotify_raw_extract")
    transform_raw_data(spotify_raw_extract)

def build_report_file(*args, **context):
    spotify_raw_extract = context.get("ti").xcom_pull(key="spotify_raw_extract")
    build_report(spotify_raw_extract)

def drop_file_to_file_store(*args, **context):
    execution_date = context['execution_date']
    file_name = "spotify_report" + str(execution_date)
    if (not transfer_file_to_drive(file_name)):
        raise ValueError('File not uploaded successfully')

## Defining the DAG
with DAG(
        dag_id="playlist_etl",
        schedule_interval="@daily",
        default_args={
            "owner": "airflow",
            "retries": 1,
            "retry_delay": timedelta(minutes=1),
            "start_date": datetime(2021, 1, 1),
        },
        catchup=False) as f:

## Define the tasks in the DAG
    download_data_from_spotify = PythonOperator(
        task_id="download_data_from_spotify",
        python_callable=download_data_from_spotify,
        provide_context=True
    )

    is_data_available = BranchPythonOperator(
        task_id='is_data_available',
        python_callable=is_data_available,
        provide_context=True
    )

    stage_raw_data_in_mongo = PythonOperator(
        task_id="stage_raw_data_in_mongo",
        python_callable=stage_raw_data_in_mongo,
        provide_context=True
    )

    no_data_available = DummyOperator(
        task_id='no_data_available'
    )

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        provide_context=True
    )

    build_report_file = PythonOperator(
        task_id="build_report_file",
        python_callable=build_report_file,
        provide_context=True
    )

    drop_file_to_file_store = PythonOperator(
        task_id="drop_file_to_file_store",
        python_callable=drop_file_to_file_store,
        provide_context=True
    )

    email_to_distro = EmailOperator(
        task_id="email_to_distro",
        to="printavf@gmail.com",
        subject="Report Published",
        html_content=""" <h3>Today's report was published</h3> """,
        dag=f
    )

    end_of_flow = DummyOperator(
        task_id='end_of_flow'
    )

download_data_from_spotify >> is_data_available >> [stage_raw_data_in_mongo, no_data_available]
no_data_available >> end_of_flow

stage_raw_data_in_mongo >> transform_data >> build_report_file >> [email_to_distro, drop_file_to_file_store] >> end_of_flow