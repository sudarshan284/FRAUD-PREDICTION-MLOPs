from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd
from typing import Union
from sklearn.model_selection import train_test_split

class DataSplitOperator(BaseOperator):
    """
    Custom Apache Airflow operator to split data into training and testing sets and save them as CSV files.
    """
    @apply_defaults
    def __init__(self, input_file:pd.DataFrame, 
                 X_train_file:pd.DataFrame, 
                 y_train_file:pd.DataFrame, 
                 X_test_file:pd.Series,
                 y_test_file: pd.Series, *args, **kwargs):
        """
        Initialize the operator.

        :param input_file: Input file path for the preprocessed data.
        :param X_train_file: Output file path for the training features.
        :param y_train_file: Output file path for the training labels.
        :param X_test_file: Output file path for the testing features.
        :param y_test_file: Output file path for the testing labels.
        """
        super(DataSplitOperator, self).__init__(*args, **kwargs)
        self.input_file = input_file
        self.X_train_file = X_train_file
        self.y_train_file = y_train_file
        self.X_test_file = X_test_file
        self.y_test_file = y_test_file

    def execute(self, context):
        self.log.info(f'Splitting data from {self.input_file} into train and test sets')

        # Retrieve the preprocessed data from the previous task using XCom
        preprocessed_data = context['ti'].xcom_pull(task_ids='data_preprocessing_task', key='preprocessed_data')

        try:
            # Load the preprocessed data from the input file
            data = pd.read_csv('data/processed/preprocessed_data.csv')
            X = data.drop(["is_fraud"],axis=1)
            y = data["is_fraud"]
            # Perform data splitting logic here
            X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.2,random_state=42)
            
            #return X_train, X_test, y_train, y_test 
            X_train.to_csv(self.X_train_file, index=False)
            y_train.to_csv(self.y_train_file, index=False) 
            X_test.to_csv(self.X_test_file, index=False)
            y_test.to_csv(self.y_test_file, index=False)

        except Exception as e:
            self.log.error(f'Data splitting failed: {str(e)}')
            raise e

# def split_data(data, test_size, random_state):
#     # Example data splitting function
#     # Modify this function to match your specific data splitting requirements
#     return X_train, y_train, X_test, y_test
