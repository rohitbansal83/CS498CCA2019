from __future__ import print_function

from pyspark.ml.classification import LinearSVC, LinearSVCModel
from pyspark.ml.classification import LogisticRegression, OneVsRest, OneVsRestModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession
import json


def predict(data, model_disease, model_level):
    risk = dict()
    disease_pred = model_disease.transform(data)
    for row in disease_pred.rdd.collect():
        if row['prediction'] == 0:
            risk[row['label']] = 'low'

    level_pred = model_level.transform(data)
    for row in level_pred.rdd.collect():
        if row['label'] not in risk:
            risk[row['label']] = 'high' if row['prediction'] == 0 else 'medium'
    return risk


if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("linearSVC Example")\
        .getOrCreate()

    # Load user data
    inputData = spark.read.format("libsvm").load("data/user_data")

    # load models
    prediction_model = LinearSVCModel.load(
        "models/HeartDisearsePredictionModel")
    level_model = OneVsRestModel.load("models/HeartDisearseLevelModel")
    risk_level = predict(inputData, prediction_model, level_model)

    with open('predict.csv', 'w') as outfile:
        for id, level in risk_level.items():
            outfile.write(str(int(id)) + ","+str(level)+"\n")
    spark.stop()
