#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

# $example on$
from pyspark.mllib.feature import PCA as PCAmllib
from pyspark.ml.feature import PCA as PCAml
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
# $example off$
from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("linearSVC Example")\
        .getOrCreate()

    # $example on$
    # Load training data
    inputData = spark.read.format("libsvm") \
        .load("combined_data_svm.txt")

    # generate the train/test split.
    (train, test) = inputData.randomSplit([0.8, 0.2])

    

    pca = PCAml(k=2, inputCol="features", outputCol="pca")
    model = PCAmllib(2).fit(train)
    transform = model.transform(train)
    predictions = model.inverse_transform(test)

   
    # score the model on test data.
    #predictions = lsvcModel.transform(test)

    # obtain evaluator.
    evaluator = MulticlassClassificationEvaluator(metricName="accuracy")

    # compute the classification error on test data.
    accuracy = evaluator.evaluate(predictions)
    print("Test Error = %g" % (1.0 - accuracy))

    # $example off$

    spark.stop()