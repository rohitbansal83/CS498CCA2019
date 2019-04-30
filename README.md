# CS498CCA2019 - An Analysis on Heart Disease
We developed a predictive model based on the combined set of data from all four the UCI Heart Disease datasets.  This model is implemented using PySpark and the associated ML Machine Learning libraries to leverage off the advantages presented by these Apache cloud infrastructure tools. 

## Implementation

1.  Clean and transform data, identify and remove outliers
2.  Transform the Combined dataset to replace all nan values with zeros and convert to svm format.
3.  Produce two distinct data sets. 
    (a) A dataset with all data points with all labels > 0 set to 1.  This dataset is used to determine the presence of heart disease. 
    (b) A dataset with all records reporting a label of > 0.  All labels > 1 are set to 0.
4.  Train a Linear SVC model on dataset (a) and save the model
5.  Train a One-vs-Rest with Logistic Regression on dataset (b) and save the model.
6.  Predict the risk of heart disease by firstly applying the Linear SVC model.  If 0 is predicted, report the sample as “Low         Risk”.  If 1 is predicted, apply the One-vs-Rest model.  If 1 is predicted, report the sample as “Medium Risk” otherwise report the sample as “High Risk”

## Running the model
To run this model the following steps must be followed:

1.  Prepare a file named _user_data_ in the _data_ sub-folder.  This file should be in the _libsvm_ format with the label field representing the sample id.
2.  Run SparkModelFit.py to generate the two models
3.  Run SparkModelPredict.py to generate prediction from _data/user_data_
4.  The results will be written to _predict.csv_.

## **Team:**

Rohit Bansal (rbansal3)
Paul Nel (paulnel2)
Alpesh Darji (adarji2)
Kahtan Al Jewary (ksa2)

