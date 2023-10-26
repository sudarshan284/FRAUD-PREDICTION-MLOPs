# FRAUD-PREDICTION-MLOPs

## Introduction
Fill the details

## Problem Statement
Fill the details

## Deployment

Let's jump into the Python packages you need. Within the Python environment of your choice, run:

```bash
git clone https://github.com/zenml-io/zenml-projects.git
cd zenml-projects/hotel-room-price
pip install -r requirements.txt
```

ZenML comes bundled with a React-based dashboard. This dashboard allows you to observe your stacks, stack components and pipeline DAGs in a dashboard interface. To access this, you need to launch the ZenML Server and Dashboard locally, but first you must install the optional dependencies for the ZenML server:

```bash
pip install zenml["server"]
pip install "zenml[server]==0.42.1"
zenml init
zenml up
```

If you are running the run_deployment.py script, you will also need to install some integrations using ZenML:

```
zenml integration install mlflow -y
```

The project can only be executed with a ZenML stack that has an MLflow experiment tracker and model deployer as a component. Configuring a new stack with the two components are as follows:

```
zenml integration install mlflow -y
zenml experiment-tracker register mlflow_trc_hrb --flavor=mlflow
zenml model-deployer register mlflow_hrb --flavor=mlflow
zenml stack register mlflow_stack_hrb -a default -o default -d mlflow_hrb -e mlflow_trc_hrb --set
```

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
