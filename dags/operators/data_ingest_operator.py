from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd

class DataIngestOperator(BaseOperator):
    @apply_defaults
    def __init__(self, input_file,ingested_data, *args, **kwargs):
        super(DataIngestOperator, self).__init__(*args, **kwargs)
        self.input_file = input_file
        self.ingested_data = ingested_data

    def execute(self, context):
        self.log.info(f'Ingesting data from {self.input_file} into the data processing pipeline')

        # Perform data ingestion logic here
        try:
            # Load data from the input file (CSV, for example)
            data = pd.read_csv(self.input_file)
            
            # You can perform additional data validation or processing as needed
            # For instance, you may want to check for missing values or perform data cleaning here.

            # Pass the ingested data to the next tasks by XCom
            #context['ti'].xcom_push(key='ingested_data', value=data)
            data.to_csv(self.ingested_data, index=False)

        except Exception as e:
            self.log.error(f'Data ingestion failed: {str(e)}')
            raise e
