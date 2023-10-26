from datetime import datetime, timedelta
from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.python import PythonOperator
from operators.data_preprocessing_operator import DataPreprocessingOperator
from operators.data_split_operator import DataSplitOperator
from operators.model_training_abc_operator import ModelTrainingABCOperator
from operators.model_training_dtc_operator import ModelTrainingDTCOperator
from operators.model_training_gbc_operator import ModelTrainingGBCOperator
from operators.model_training_rfc_operator import ModelTrainingRFCOperator
from operators.model_evaluation_abc_operator import ModelEvaluationABCOperator
from operators.model_evaluation_dtc_operator import ModelEvaluationDTCOperator
from operators.model_evaluation_gbc_operator import ModelEvaluationGBCOperator
from operators.model_evaluation_rfc_operator import ModelEvaluationRFCOperator
from operators.model_prediction_operator import ModelPredictionOperator
from operators.data_download_operator import downloadFromBlobStorage
from operators.data_upload_operator import uploadToBlobStorage
from operators.model_selection_operator import modelselection

# Default arguments for the DAG
default_args = {
    'owner': 'admin',
    'start_date': datetime(2023, 1, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG instance
dag = DAG(
    dag_id='azure_fraud_detection_dag',
    default_args=default_args,
    description='End-to-End Fraud Detection Pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# Define tasks

# Data Ingestion Task
# Data Ingestion To BlobStorage 
data_upload_task = PythonOperator(
    task_id='data_upload_task',
    python_callable=uploadToBlobStorage,
    dag=dag,
)

# Data download From BlobStorage 
data_download_task = PythonOperator(
    task_id='data_download_task',
    python_callable=downloadFromBlobStorage,
    dag=dag,
)

# Data Preprocessing Task
data_preprocessing_task = DataPreprocessingOperator(
    task_id='data_preprocessing_task',
    #input_file=data_ingest_task.output,
    preprocessed_data='data/processed/preprocessed_data.csv',
    dag=dag,
)

# Data Splitting Task
data_split_task = DataSplitOperator(
    task_id='data_split_task',
    input_file=data_preprocessing_task.output,
    X_train_file='data/processed/X_train.csv',
    y_train_file='data/processed/y_train.csv',
    X_test_file='data/processed/X_test.csv',
    y_test_file='data/processed/y_test.csv',
    dag=dag,
)


# AdaBoostClassifier Model Training Task
model_training_abc_task = ModelTrainingABCOperator(
    task_id='model_training_abc_task',
    X_train_file=data_split_task.X_train_file,
    y_train_file=data_split_task.y_train_file,
    model_file='models/abc_model.pkl',
    dag=dag,
)
# DecisionTreeClassifier Model Training Task
model_training_dtc_task = ModelTrainingDTCOperator(
    task_id='model_training_dtc_task',
    X_train_file=data_split_task.X_train_file,
    y_train_file=data_split_task.y_train_file,
    model_file='models/dtc_model.pkl',
    dag=dag,
)

# GradientBoostingClassifier Model Training Task
model_training_gbc_task = ModelTrainingGBCOperator(
    task_id='model_training_gbc_task',
    X_train_file=data_split_task.X_train_file,
    y_train_file=data_split_task.y_train_file,
    model_file='models/gbc_model.pkl',
    dag=dag,
)

# RandomForestClassifier Model Training Task
model_training_rfc_task = ModelTrainingRFCOperator(
    task_id='model_training_rfc_task',
    X_train_file=data_split_task.X_train_file,
    y_train_file=data_split_task.y_train_file,
    model_file='models/rfc_model.pkl',
    dag=dag,
)


# AdaBoostClassifier Model Evaluation Task
model_evaluation_abc_task = ModelEvaluationABCOperator(
    task_id='model_evaluation_abc_task',
    X_test_file=data_split_task.X_test_file,
    y_test_file=data_split_task.y_test_file,
    model_file='models/abc_model.pkl',
    output_file='models/result/evaluation_abc_results.txt',
    dag=dag,
)

# DecisionTreeClassifier Model Evaluation Task
model_evaluation_dtc_task = ModelEvaluationDTCOperator(
    task_id='model_evaluation_dtc_task',
    X_test_file=data_split_task.X_test_file,
    y_test_file=data_split_task.y_test_file,
    model_file='models/dtc_model.pkl',
    output_file='models/result/evaluation_dtc_results.txt',
    dag=dag,
)
# GradientBoostingClassifier Model Evaluation Task
model_evaluation_gbc_task = ModelEvaluationGBCOperator(
    task_id='model_evaluation_gbc_task',
    X_test_file=data_split_task.X_test_file,
    y_test_file=data_split_task.y_test_file,
    model_file='models/gbc_model.pkl',
    output_file='models/result/evaluation_gbc_results.txt',
    dag=dag,
)

# RandomForestClassifier Model Evaluation Task
model_evaluation_rfc_task = ModelEvaluationRFCOperator(
    task_id='model_evaluation_rfc_task',
    X_test_file=data_split_task.X_test_file,
    y_test_file=data_split_task.y_test_file,
    model_file='models/rfc_model.pkl',
    output_file='models/result/evaluation_rfc_results.txt',
    dag=dag,
)

# Model Selection Task
model_selection_task = PythonOperator(
    task_id='model_selection_task',
    python_callable=modelselection,
    dag=dag,
)

# Model Prediction Task
model_prediction_task = ModelPredictionOperator(
    task_id='model_prediction_task',
    input_file='data/raw/Test.csv',
    model_file='models/final_model.pkl',
    output_file='models/result/prediction_result.txt',
    dag=dag,
)

# Set up task dependencies
chain(data_upload_task , data_download_task , data_preprocessing_task , data_split_task , [model_training_abc_task, model_training_dtc_task, model_training_gbc_task, model_training_rfc_task] , [model_evaluation_abc_task, model_evaluation_dtc_task, model_evaluation_gbc_task, model_evaluation_rfc_task]  , model_selection_task, model_prediction_task)