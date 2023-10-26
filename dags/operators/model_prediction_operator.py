from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
import joblib
import calendar

class ModelPredictionOperator(BaseOperator):
    """
    Custom Apache Airflow operator to evaluate a machine learning model and save evaluation results to a file.
    """

    @apply_defaults
    def __init__(self, input_file, model_file, output_file, *args, **kwargs):
        """
        Initialize the operator.

        :param X_test_file: File path to the features of the testing set (X_test).
        :param y_test_file: File path to the labels of the testing set (y_test).
        :param model_file: File path to load the trained model.
        :param output_file: File path to save the evaluation results.
        """
        super(ModelPredictionOperator, self).__init__(*args, **kwargs)
        self.input_file = input_file
        self.model_file = model_file
        self.output_file = output_file

    def execute(self, context):
        self.log.info(f'Evaluating the machine learning model using data from {self.input_file}')

        try:
            """
            Execute the operator to evaluate a machine learning model and save evaluation results to a file.
            """
            # Load the testing data and trained model from the provided files
            new_data = pd.read_csv('data/raw/Test.csv')
            new_data['trans_date_trans_time'] = pd.to_datetime(new_data['trans_date_trans_time'], format='%d-%m-%Y %H:%M')
            new_data['trans_date']=new_data['trans_date_trans_time'].dt.strftime('%Y-%m-%d')
            new_data['trans_date']=pd.to_datetime(new_data['trans_date'])
            new_data['dob']=pd.to_datetime(new_data['dob'],format='%d-%m-%Y')
            new_data["age"] = new_data["trans_date"]-new_data["dob"]
            new_data["age"] = new_data["age"].astype('int64')
            new_data['trans_month'] = pd.DatetimeIndex(new_data['trans_date']).month
            new_data['trans_year'] = pd.DatetimeIndex(new_data['trans_date']).year
            new_data['Month_name'] = new_data['trans_month'].apply(lambda x: calendar.month_abbr[x])
            new_data['latitudinal_distance'] = abs(round(new_data['merch_lat']-new_data['lat'],3))
            new_data['longitudinal_distance'] = abs(round(new_data['merch_long']-new_data['long'],3))
            new_data.gender=new_data.gender.apply(lambda x: 1 if x=="M" else 0)
            new_data = new_data.drop(['cc_num','merchant','first','last','street','zip','trans_num','unix_time','trans_date_trans_time','city','lat','long','job','dob','merch_lat','merch_long','trans_date','state','Month_name'],axis=1)
            new_data =pd.get_dummies(new_data,columns=['category'],drop_first=True)

            X_new = new_data.drop(["is_fraud"],axis=1)
            y_new = new_data["is_fraud"]
            model = joblib.load(self.model_file)

            # Make predictions using the trained model
            y_pred_new = model.predict(X_new)
            print('y_new', y_new)
            print('y_pred_new',y_pred_new)
            # Calculate and print evaluation metrics
            accuracy = accuracy_score(y_new, y_pred_new)
            classification_rep = classification_report(y_new, y_pred_new, target_names=['class_0', 'class_1'])  # Customize labels as needed

            # Save evaluation results to the specified output file
            with open(self.output_file, 'w') as f:
                f.write(f"Accuracy: {accuracy}\n\nClassification Report:\n{classification_rep}")

        except Exception as e:
            self.log.error(f'Model evaluation failed: {str(e)}')
            raise e
