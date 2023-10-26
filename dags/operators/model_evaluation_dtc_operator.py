from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
import joblib

class ModelEvaluationDTCOperator(BaseOperator):
    """
    Custom Apache Airflow operator to evaluate a machine learning model and save evaluation results to a file.
    """

    @apply_defaults
    def __init__(self, X_test_file, y_test_file, model_file, output_file, *args, **kwargs):
        """
        Initialize the operator.

        :param X_test_file: File path to the features of the testing set (X_test).
        :param y_test_file: File path to the labels of the testing set (y_test).
        :param model_file: File path to load the trained model.
        :param output_file: File path to save the evaluation results.
        """
        super(ModelEvaluationDTCOperator, self).__init__(*args, **kwargs)
        self.X_test_file = X_test_file
        self.y_test_file = y_test_file
        self.model_file = model_file
        self.output_file = output_file

    def execute(self, context):
        self.log.info(f'Evaluating the machine learning model using data from {self.X_test_file,self.y_test_file }')

        # Retrieve the test data from the previous task using XCom
        test_data = context['ti'].xcom_pull(task_ids='data_split_task', key='test_data')

        try:
            """
            Execute the operator to evaluate a machine learning model and save evaluation results to a file.
            """
            # Load the testing data and trained model from the provided files
            X_test = pd.read_csv(self.X_test_file)
            y_test = pd.read_csv(self.y_test_file)
            model = joblib.load(self.model_file)

            # Make predictions using the trained model
            y_pred = model.predict(X_test)

            # Calculate and print evaluation metrics
            accuracy = accuracy_score(y_test, y_pred)
            classification_rep = classification_report(y_test, y_pred, target_names=['class_0', 'class_1'])  # Customize labels as needed

            # Save evaluation results to the specified output file
            with open(self.output_file, 'w') as f:
                f.write(f"Accuracy: {accuracy}\n\nClassification Report:\n{classification_rep}")

        except Exception as e:
            self.log.error(f'Model evaluation failed: {str(e)}')
            raise e
