from __future__ import print_function

from pyspark.ml.classification import LinearSVC, LinearSVCModel
from pyspark.ml.classification import LogisticRegression, OneVsRest, OneVsRestModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession

def predict(record, m1, m2):
    predicted = m1.transform(record)
    value = predicted.select('prediction').collect()
    if int(value[0].prediction) == 0:
        return "low"
    else:
        predicted = m2.transform(record)
        value = predicted.select('prediction').collect()
        if int(value[0].prediction) == 0:
            return "high"
        else:
            return "medium"

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("linearSVC Example")\
        .getOrCreate()

    # Load user data
    inputData = spark.read.format("libsvm").load("user_data")

    # load models
    lsvcModel = LinearSVCModel.load("HeartDisearsePredictionModel")
    ovrModel = OneVsRestModel.load("HeartDisearseLevelModel")
        
    # hd prediction
    predictions_hd = lsvcModel.transform(inputData)
    predictions_hd.rdd.saveAsTextFile('hd_prediction')

    # hd level prediction
    predictions_lv = ovrModel.transform(inputData)
    predictions_lv.rdd.saveAsTextFile('hd_level')
    
    spark.stop()