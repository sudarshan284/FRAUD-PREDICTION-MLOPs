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
![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/f2c7a96a-300d-497c-aa68-91f3315a2ca9)

Airflow, an open source Apache Software Foundation workflow management platform, is used to automate, schedule, and monitor workflows. Airflow workflows are defined as directed acyclic graphs (DAGs). DAGs are made up of tasks that are executed in a specific order. Airflow provides a number of features that make it a good choice for workflow management, including:

* ``Scalability:`` Airflow can be scaled to handle a large number of tasks and workflows.

* ``Reliability:`` Airflow is designed to be reliable and fault-tolerant.

* ``Flexibility:`` Airflow can be used to automate a wide variety of workflows, from simple to complex.

* ``Extensibility:`` Airflow can be easily extended to meet the needs of specific organizations.

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


![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/61d2d37f-c9df-4429-8884-deec5493f500)


In this project we will be using MS Azure, to fetch the data from storage container. Use below link for reference.


```https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal```

![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/59c5ac0a-e801-43d8-a3dd-edce5d12c01b)


## Solution
In real world build a model is not enough, we have to deploy the model into the production and monitor the model performance over time and how it is interacting with real world data. So, I build an end-to-end pipeline for continuously predicting and deploying the machine learning model alongside a data application that utilizes the latest deployed model for the business to consume. This way can track our production ready model. I highly suggest you to refer ZenML document for more details.

Using Airflow we can monitor the logs in real-time as well as old logs can also be checked.

I will show how I used Airflow pipeline to create a model that uses past transactions data to predict the fraud transactions for customer or third parties. I aslo deployed a Streamlit application to showcase the final end product.


## Training dataset
We have used the dataset from the kaggle.The dataset contains more than 10 million training record on which we will train-test the model.We also have half million test record on which model we will perform perdiction. This dataset is the imbalance dataset as fraud transaction are very less comapre to the valid transaction.The sample dataset includes various details,below are the details:

* ``trans_date_trans_time``:- Transaction DateTime

* ``cc_num`` - Credit Card Number of Customer

* ``merchant`` - Merchant Name

* ``category`` - Category of Merchant

* ``amt`` - Amount of Transaction

* ``first`` - First Name of Credit Card Holder

* ``last`` - Last Name of Credit Card Holder

* ``gender`` - Gender of Credit Card Holder

* ``street`` - Street Address of Credit Card Holder

* ``city`` - City of Credit Card Holder

* ``state`` - State of Credit Card Holder

* ``zip`` - Zip of Credit Card Holder

* ``lat`` - Latitude Location of Credit Card Holder

* ``long`` - Longitude Location of Credit Card Holder

* ``city_pop`` - Credit Card Holder's City Population

* ``job`` - Job of Credit Card Holder

* ``dob`` - Date of Birth of Credit Card Holder

* ``trans_num`` - Transaction Number

* ``unix_time`` - UNIX Time of transaction

* ``merch_lat`` - Latitude Location of Merchant

* ``merch_long`` - Longitude Location of Merchant

* ``is_fraud`` - Fraud Flag <--- Target Class


## Training Pipeline
Our standard training pipeline consists of several steps:
* ``data_upload_operator``:- This operator will take the file from local storage and upload it into the azure blob container.

* ``data_download_operator``:- This operator will download the file from the azure to local storage.

* ``data_preprocessing_operator``:- This operator performs the preprocessing on the dataset downloaded from azure. Since our dataset imbalanced once data clearing is completed, we will use undersampling or oversampling techniques.

* ``data_split_operator``:- This operator will split the dataset into two part. On first part the model will be trained and on second set model will be tested.

* ``model_training_operator``:- This operator is used to train model on dataset.

* ``model_evaluation_operator``:- This operator is used to evaluate the model performance.

Below is the pipeline workflow which we will implement in this project.
![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/81f2bd60-dcd0-44bb-91ea-f348dd65420b)


## Model Selection Pipeline
In model training pipeline we have used ensemble learning with DecisionTreeClassifier, RandomForestClassifier, AdaBoostClassifier and GradientBoostingClassifier. Once model training is completed then model evaluatoin will be executed. Then we will created model selection pipeline which compare the model and select the best model.

* ``model_selection_operator``:- In model training operator we used multiple ML algorithm to train model. In this operator we will compare the different model and choose the best model. 

## Model Prediction Pipeline
As we have half million test record on which model is neither training or tested. We will use this data set to check how good is our model.  

* ``model_prediction_operator``:- This operator is used to predict the model on new unseen dataset.

## Model Monitoring and Log Analysis

Airflow also offer the feature to monitor our model in real-time. When the DAGs are executed there are different status through which it passes.Below is status code show.  
![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/c6f942af-ad8b-45c3-be13-52300a737b24)

In Airflow we can also monitor the logs, DAGS generate log when the pipeline is executed. Below is the image.
![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/122eaa72-a56b-43f1-b4a0-cf55487ba226)

## Demo Streamlit App ![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/85fbe63c-37e7-4757-af9b-7d15127ef02a) 


There is a live demo of this project using Streamlit which you can find here. It takes some input features for the product and predicts the customer satisfaction rate using the latest trained models. If you want to run this Streamlit app in your local system, you can run the following command to access the app locally.

``streamlit run streamlit_app.py``

The cloud version of app can also be accessed using below url.

```
https://fraud-prediction-mlops-d8rcgc2prmv9xapx5ahhhn.streamlit.app/
```

Below is the sample model result.

![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/011aa5d8-d32b-491d-9d2c-cb177db6c7e2) ![image](https://github.com/ashishk831/FRAUD-PREDICTION-MLOPs/assets/81232686/62f6ea06-c1ba-454d-8ed7-a046382930e2)


