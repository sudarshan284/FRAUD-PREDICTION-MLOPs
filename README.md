# FRAUD-PREDICTION-MLOPs

## Introduction
In todays world with the increase in digitalization the digital transactions are also increasing and so the frauds.The Fraud transaction are increasing at 27% per year around the world.In one day there is more than 50 million transactions take place in USA alone,so predicting the fraud transaction is a difficult task.This posses a great challenge for banks,customer as well as governments.This project focus on detecting the fraud transaction using Machine learning techniques.

## Problem Statement
In this project we will build a model that will predict the fraud transaction in real-time. This prediction would help to identify whether the transaction is valid or not to help the customer or other parties.By analyzing this information companies can provide the better service and good customer experience.


## Deployment

Let's jump into the Python packages you need. Within the Python environment of your choice, run:

```bash
git clone https://github.com/apache/airflow
cd airflow-projects/fraud-prediction
pip install -r requirements.txt
```

Airflow comes bundled with a React-based dashboard. This dashboard allows you to observe your stacks, stack components and pipeline DAGs in a dashboard interface. To access this, you need to launch the Airflow Server and Dashboard locally, but first you must install the optional dependencies for the Airflow server:

```bash
#Installing airflow
pip install 'apache-airflow==2.7.1' \ --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.1/constraints-3.8.txt"
#Setting home path
export AIRFLOW_HOME=/c/Users/[YourUsername]/airflow
#Initialize the database:
airflow db init
#Create an Airflow User
airflow users create --username admin –password admin –firstname admin –lastname admin –role Admin –email youremail@email.com
#Check the created user
airflow users list
#Run the Webserver
#Run the scheduler
airflow scheduler

#If the default port 8080 is in use, change the port by typing:
airflow webserver –port <port number>
```

Login to the Airflow dashboard using the username and password created above. 

![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/35016988-aa8a-44cb-9d21-2b5beb2fc9f4)


In this project we will be using MS Azure, to fetch the data from storage container. Use below link for reference.
https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal

![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/59c5ac0a-e801-43d8-a3dd-edce5d12c01b)


## Solution
Fill the details

## Training dataset
The sample dataset includes various details about each order, such as:
* ``Arrival details``: Arrival year,Arrival month,Arrival week,Arrival day of month
* ``Stay details``: Week nights stay ,Weekend nights stay.
* ``Person details``: Adults, Children, Babies.
* ``Cancellation details``: Previous cancellations,No previous cancellations.
* ``Room type details``:Reserved room,Assigned room,Booking changes.
* ``Facilites``: Meal,Car parking and etc.

## Training Pipeline
Our standard training pipeline consists of several steps:
* ``ingest_data()``:- This methods will take the dataset location as an argument and convert it into a dataframe.
* ``clean_data()``: - This method will clean the data and remove the unwanted columns. It fills null values with median and remove outliers.
* ``train_model()``: - This step will train models linear regression. I am also using MLflow to track our model performance, parameters, metrics and for saving the model.
* ``evaluate_model()``: -  This step will evaluate the model and save the metrics using MLflow autologging into the artifact store. Autologging can be used to compare the performance of different models and decide to select the best model. 

## Deployment Pipeline
Fill the details
The first four steps of the pipeline are the same as above, but we have added the following additional ones:
* ``deployment_trigger``: The step checks whether the newly trained model meets the criteria set for deployment.
* ``model_deployer``: This step deploys the model as a service using MLflow (if deployment criteria is met).

## Executing Code
We can run two pipelines as follows:

* Training pipeline:
`` python run_pipeline.py`` 
* The continuous deployment pipeline:
``python run_deployment.py``
## Demo Streamlit App
There is a live demo of this project using Streamlit which you can find here. It takes some input features for the product and predicts the customer satisfaction rate using the latest trained models. If you want to run this Streamlit app in your local system, you can run the following command:

``streamlit run streamlit_app.py``
