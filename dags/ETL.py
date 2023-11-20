from datetime import datetime
import sys
import csv
import json
import os
import pandas as pd 
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.bash import BashOperator
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python import PythonOperator

def data_transform_and_load():
    #spécifier le chemin vers le fichier CSV
    csv_file_path_sos = os.path.expandvars("${AIRFLOW_HOME}/data/donnees-urgences-SOS-medecins.csv")
    df_urgences = pd.read_csv(csv_file_path_sos, delimiter=';', dtype={'Code tranches d\'age': str})

    csv_file_path_age = os.path.expandvars("${AIRFLOW_HOME}/data/code-tranches-dage-donnees-urgences.csv")
    df_age = pd.read_csv(csv_file_path_age, delimiter=",")
    
    json_file_path_departements = os.path.expandvars("${AIRFLOW_HOME}/data/departements-region.json")
    with open(json_file_path_departements, 'r',encoding="UTF-8") as json_file:
        data = json.load(json_file)
        df_departements = pd.DataFrame(data)
    
    
    #transformations
    #fichier 1 donnes-urgences-SOS-medecins.csv
    #1- Uniformisations des dates
    df_urgences['date_de_passage']= pd.to_datetime(df_urgences['date_de_passage'],errors = 'coerce')
    df_urgences['date_de_passage']= df_urgences['date_de_passage'].dt.strftime('%Y-%m-%d') 
    # Remplacer les valeurs manquantes par une valeur par défaut
    df_urgences.columns = df_urgences.columns.str.strip() # supp des espaces 
    
    df_urgences = df_urgences.drop_duplicates().reset_index(drop=True) #supp des lignes en doublons :
    #columns_to_convert = ['dep', 'sursaud_cl_age_corona', 'nbre_pass_corona', 'nbre_pass_tot', 'nbre_hospit_corona',
                         #'nbre_pass_corona_h', 'nbre_pass_corona_f', 'nbre_pass_tot_h', 'nbre_pass_tot_f',
                         #'nbre_hospit_corona_h', 'nbre_hospit_corona_f', 'nbre_acte_corona', 'nbre_acte_tot',
                         #'nbre_acte_corona_h', 'nbre_acte_corona_f', 'nbre_acte_tot_h', 'nbre_acte_tot_f']

    #df_urgences['columns_to_convert'] = df_urgences['columns_to_convert'].apply(pd.to_numeric, errors='coerce')
   # df_urgences['columns_to_convert'] = df_urgences['columns_to_convert'].fillna(0) 

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
        python_callable= data_transform_and_load
    )
    
    create_table = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_connexion',
    sql='sql/create_table.sql'
    )


"HELLO"
print(sys.executable)
extract_task





def data_transform_and_load():
    df = pd.read_csv(os.path.expandvars("${AIRFLOW_HOME}/data/valeurs_foncieres.txt" ), 
                     sep="|", 
                     dtype="unicode", 
                     usecols = ["Type local", "Valeur fonciere", "Code commune", "Surface reelle bati" ]) 
      
    df = df[df["Type local"] == "Appartement"]
    df["Valeur fonciere"] = df["Valeur fonciere"].str.replace(',', '.').astype(float)
    df["prix par m2"] = df["Valeur fonciere"] / df["Surface reelle bati"].astype(float)
    
    result = df.groupby(["Code commune"]).aggregate(prix_moyen = ('prix par m2','mean')).reset_index()
    result = result.round(0)

    postgres_sql_upload = PostgresHook(postgres_conn_id="postgres_connexion")
    result.to_sql('analyse_prix', postgres_sql_upload.get_sqlalchemy_engine(), if_exists='replace', chunksize=1000)

    return 



default_args = {
    'owner': 'airflow',
    'depends_on_past': False
    }

with DAG(
    'ETL',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    
) as dag:
    
    extract = BashOperator(
        task_id='Extract',
        bash_command='curl --keepalive-time 6000 -o ${AIRFLOW_HOME}/data/valeurs_foncieres.txt ',
    )

    create_table = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_connexion',
    sql='sql/create_table.sql'
    )
    
    transform_and_load = PythonOperator(
    task_id = 'transform_and_load',
    python_callable = data_transform_and_load
    )


    [extract, create_table] >> transform_and_load

