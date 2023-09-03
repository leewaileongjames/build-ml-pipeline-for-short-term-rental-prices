# Project 2 - Build a ML Pipeline for Short term Rental Prices in NYC


Reference: [ML DevOps Engineer Nanodegree](https://www.udacity.com/course/machine-learning-dev-ops-engineer-nanodegree--nd0821) by Udacity.

## Description

This project is part of Module 2: ***Building a Reproducible Model Workflow***.

* We are working for a property management company renting rooms and properties for short periods of time on various rental platforms
* We need to estimate the typical price for a given property based on the price of similar properties
* Our company receives new data in bulk every week. Therefore, our model needs to be retrained with the same cadence, necessitating an end-to-end pipeline that can be reused.

## Prerequisites

1. Linux environment with miniconda and python installed
2. **(Optional)** Change the default solver for conda to conda-libmamba-solver. More information is available [here](https://www.anaconda.com/blog/conda-is-fast-now).

## Installing the Initial Environment
```bash
# Clone the git repo
git clone https://github.com/leewaileongjames/build-ml-pipeline-for-short-term-rental-prices.git
cd build-ml-pipeline-for-short-term-rental-prices

# Install the initial environment
conda env create -f environment.yml
```

## How to use the pipeline

Every step of the MLflow pipeline is run within an isolated conda environment. ***Here is the link to the [project](https://wandb.ai/leewljames/nyc_airbnb) in W&B.***

The entire pipeline can be run like this:
```bash
# Ensure that you are within the 
# "build-ml-pipeline-for-short-term-rental-prices" directory

mlflow run .
```

Alternatively, you may run specific steps of the pipeline. For example:
```bash
# Running only the "download" step
mlflow run . -P steps=download

# Running only the "download" & "basic_cleaning" steps
mlflow run . -P steps=download,basic_cleaning
```

You may also override the default parameter values using the Hydra syntax:
```bash
mlflow run . \
  -P steps=download,basic_cleaning \
  -P hydra_options="modeling.random_forest.n_estimators=10 etl.min_price=50"
```

**Note:** The default parameter values are defined in the ***config.yml*** file

<br/>

**Here is a list of steps (in sequence) available within the pipeline:**
- **download** - Uploads the dataset from local machine to W&B project
- **basic_cleaning** - Performs data processing on the dataset
- **data_check** - Validates the dataset
- **data_split** - Splits the dataset into 'trainval' and 'test' and upload onto W&B
- **train_random_forest** - Creates a sklearn pipeline that trains a random forest model using the trainval dataset. Uploads the inference artifact onto W&B.
- **test_regression_model** - Evaluates the performance of the inference artifact against the test dataset

<br/>

**EDA:**

You may run the following command to perform EDA using a JupyterLab environment
```bash
# Ensure that you are within the 
# "build-ml-pipeline-for-short-term-rental-prices" directory

mlflow run src/eda
```

<br />

**Optimize hyperparameters**

You may perform a grid search across multiple hyperparameters in order to optimize your model. For example:
```bash
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.random_forest.max_depth=10,50,100 modeling.random_forest.n_estimators=100,200,500 -m"
```

