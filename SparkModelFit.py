#--------------------------------------------------
#  Spark Application to Fit Linear Regression model
#  on Heart Disease Dataset
#--------------------------------------------------

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator


DEBUG = True

spark = SparkSession \
    .builder \
    .appName("Heart Disease Model Fit") \
    .getOrCreate()
	

columns = ["age", "sex", "cp", "restecg", "thalach", "exang", "setid", "label"]
exclude = ["label"]
	
df = spark.read.format("csv").options(header="false", inferschema="true").load("combined_data.txt")
df = df.toDF(*columns)

VA = VectorAssembler(inputCols = [feature for feature in columns if feature not in exclude], \
                     outputCol = 'features')
df = VA.transform(df)
df = df.select(['features', 'label'])
df.show(3)

splits = df.randomSplit([0.7, 0.3])
train_df = splits[0]
test_df = splits[1]

lr = LinearRegression(featuresCol = 'features', labelCol='label', maxIter=10, regParam=0.3, \
                      elasticNetParam=0.8)
lr_model = lr.fit(train_df)
if DEBUG: print("Coefficients: " + str(lr_model.coefficients))
if DEBUG: print("Intercept: " + str(lr_model.intercept))

trainingSummary = lr_model.summary
if DEBUG: print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
if DEBUG: print("r2: %f" % trainingSummary.r2)

lr_predictions = lr_model.transform(test_df)
lr_predictions.select("prediction","label","features").show(5)
lr_evaluator = RegressionEvaluator(predictionCol="prediction", labelCol="label", metricName="r2")
if DEBUG: print("R Squared (R2) on test data = %g" % lr_evaluator.evaluate(lr_predictions))

test_result = lr_model.evaluate(test_df)
if DEBUG: print("Root Mean Squared Error (RMSE) on test data = %g" % test_result.rootMeanSquaredError)

if DEBUG: print("numIterations: %d" % trainingSummary.totalIterations)
if DEBUG: print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
if DEBUG: trainingSummary.residuals.show()

# save model
lr_model.write().overwrite().save("HeartDisearsePredictionModel")
