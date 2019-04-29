from __future__ import print_function

from pyspark.ml.classification import LinearSVC
from pyspark.ml.classification import LogisticRegression, OneVsRest
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession

DEBUG = False
if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("linearSVC Example")\
        .getOrCreate()

    # Load binary training data (heart disease = YES or NO)
    inputData = spark.read.format("libsvm").load("combined_hd_absence")

    if DEBUG:
        # generate the train/test split.
        (train, test) = inputData.randomSplit([0.8, 0.2])
    else:
        train = inputData

    lsvc = LinearSVC(maxIter=10, regParam=0.1)

    # Fit the model
    lsvcModel = lsvc.fit(train)

    if DEBUG:
        # score the model on test data.
        #test = spark.read.format("libsvm").load("user_data")
        predictions = lsvcModel.transform(test)
        # predictions.rdd.saveAsTextFile('test1')

        # obtain evaluator.
        evaluator = MulticlassClassificationEvaluator(metricName="accuracy")

        # compute the classification error on test data.
        accuracy = evaluator.evaluate(predictions)
        print("Test Error = %g" % (1.0 - accuracy))

    # Load binary training data (heart disease level = MEDIUM or HIGH)
    inputData = spark.read.format("libsvm").load("combined_hd_level")

    if DEBUG:
        # generate the train/test split.
        (train, test) = inputData.randomSplit([0.8, 0.2])
    else:
        train = inputData

    # instantiate the base classifier.
    lr = LogisticRegression(maxIter=10, tol=1E-6, fitIntercept=True)

    # instantiate the One Vs Rest Classifier.
    ovr = OneVsRest(classifier=lr)

    # train the multiclass model.
    ovrModel = ovr.fit(train)

    if DEBUG:
        # score the model on test data.

        predictions = ovrModel.transform(test)
        print(predictions.select('label', 'prediction').show(20))

        # obtain evaluator.
        evaluator = MulticlassClassificationEvaluator(metricName="accuracy")

        # compute the classification error on test data.
        accuracy = evaluator.evaluate(predictions)
        print("Test Error = %g" % (1.0 - accuracy))

    if not DEBUG:
        # save model
        lsvcModel.write().overwrite().save("HeartDisearsePredictionModel")
        ovrModel.write().overwrite().save("HeartDisearseLevelModel")

    spark.stop()
