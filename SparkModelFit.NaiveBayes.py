# --------------------------------------------------
#  Spark Application to Fit Linear Regression model
#  on Heart Disease Dataset
# --------------------------------------------------

import shutil
from pyspark import SparkContext
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.util import MLUtils
from pyspark.mllib.feature import StandardScaler
from pyspark.mllib.regression import LabeledPoint

sc = SparkContext(appName="HeartDiseaseModelFit")

# Load and parse the data file.
data = MLUtils.loadLibSVMFile(sc, "data/combined_hd_base")

# Split data approximately into training (60%) and test (40%)
training, test = data1.randomSplit([0.7, 0.3])

# Train a naive Bayes model.
model = NaiveBayes.train(training, 1.0)

# Make prediction and test accuracy.
predictionAndLabel = test.map(lambda p: (model.predict(p.features), p.label))
accuracy = 1.0 * \
    predictionAndLabel.filter(lambda pl: pl[0] == pl[1]).count() / test.count()
print('model accuracy {}'.format(accuracy))

# Save and load model
output_dir = './myNaiveBayesModel'
shutil.rmtree(output_dir, ignore_errors=True)
model.save(sc, output_dir)
sameModel = NaiveBayesModel.load(sc, output_dir)
predictionAndLabel = test.map(lambda p: (
    sameModel.predict(p.features), p.label))
accuracy = 1.0 * \
    predictionAndLabel.filter(lambda pl: pl[0] == pl[1]).count() / test.count()
print('sameModel accuracy {}'.format(accuracy))
