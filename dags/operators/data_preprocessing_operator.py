from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd
import calendar

class DataPreprocessingOperator(BaseOperator):
    @apply_defaults
    def __init__(self, preprocessed_data, *args, **kwargs): #input_file:pd.DataFrame,
        super(DataPreprocessingOperator, self).__init__(*args, **kwargs)
        #self.input_file = input_file
        self.preprocessed_data = preprocessed_data

    def execute(self, context):
        #self.log.info(f'Performing data preprocessing for {self.input_file}')

        # Retrieve the ingested data from the previous task using XCom
        #ingested_data = context['ti'].xcom_pull(task_ids='data_ingest_task', key='ingested_data')

        try:
            # Perform data preprocessing logic here
            # For example, you can clean, transform, or engineer features in the ingested data
            data = pd.read_csv('data/processed/ingested_data.csv')
            data['trans_date_trans_time'] = pd.to_datetime(data['trans_date_trans_time'], format='%d-%m-%Y %H:%M')
            data['trans_date']=data['trans_date_trans_time'].dt.strftime('%Y-%m-%d')
            data['trans_date']=pd.to_datetime(data['trans_date'])
            data['dob']=pd.to_datetime(data['dob'],format='%d-%m-%Y')
            data["age"] = data["trans_date"]-data["dob"]
            data["age"] = data["age"].astype('int64')
            data['trans_month'] = pd.DatetimeIndex(data['trans_date']).month
            data['trans_year'] = pd.DatetimeIndex(data['trans_date']).year
            data['Month_name'] = data['trans_month'].apply(lambda x: calendar.month_abbr[x])
            data['latitudinal_distance'] = abs(round(data['merch_lat']-data['lat'],3))
            data['longitudinal_distance'] = abs(round(data['merch_long']-data['long'],3))
            data.gender=data.gender.apply(lambda x: 1 if x=="M" else 0)
            data = data.drop(['cc_num','merchant','first','last','street','zip','trans_num','unix_time','trans_date_trans_time','city','lat','long','job','dob','merch_lat','merch_long','trans_date','state','Month_name'],axis=1)
            data =pd.get_dummies(data,columns=['category'],drop_first=True)

            #Performing Undersampling
            normal = data[data['is_fraud']==0]
            fraud = data[data['is_fraud']==1]
            normal_sample=normal.sample(n=len(fraud),random_state=42)
            new_data = pd.concat([normal_sample,fraud],ignore_index=True)

            #Performing Oversampling
            # normal = data[data['is_fraud']==0]
            # fraud = data[data['is_fraud']==1]
            # fraud_sample=fraud.sample(n=len(normal),replace=True,random_state=42)
            # new_data = pd.concat([normal,fraud_sample],ignore_index=True)
            
            # Save the preprocessed data to the output file (e.g., a CSV file)
            new_data.to_csv(self.preprocessed_data, index=False)

        except Exception as e:
            self.log.error(f'Data preprocessing failed: {str(e)}')
            raise e
