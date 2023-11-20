from datetime import datetime
import sys
import csv
import pandas as pd 
import os
from airflow.hooks.postgres_hook import PostgresHook
import json

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def extract_data():
    #spécifier le chemin vers le fichier CSV
    csv_file_path_sos = os.path.expandvars("${AIRFLOW_HOME}/data/donnees-urgences-SOS-medecins.csv")
    df_urgences = pd.read_csv(csv_file_path_sos, delimiter=';', dtype={'Code tranches d\'age': str})


    csv_file_path_age = os.path.expandvars("${AIRFLOW_HOME}/data/code-tranches-dage-donnees-urgences.csv")
    df_age = pd.read_csv(csv_file_path_age, delimiter=",")
    
    json_file_path_departements = os.path.expandvars("${AIRFLOW_HOME}/data/departements-region.json")
    with open(json_file_path_departements, 'r',encoding="UTF-8") as json_file:
        data = json.load(json_file)
        df_departements = pd.DataFrame(data)
    print(df_age)
    print(df_departements)
    # Retourner les DataFrames pour les rendre accessibledop en dehors de la fonction
    return df_age, df_urgences, df_departements

default_args = {
    'owner': 'airflow',
    'depends_on_past': False
}

with DAG(
    'Projet',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
) as dag:

    # Utiliser un PythonOperator pour appeler la fonction extract_data
    extract_task = PythonOperator(
        task_id='Extract',
        python_callable=extract_data
    )


"HELLO izane"
print(sys.executable)
extract_task
