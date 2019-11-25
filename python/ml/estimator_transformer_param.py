from __future__ import print_function
from pyspark.ml import Pipeline
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import StringIndexer, OneHotEncoderEstimator, VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("EstimatorTransformerParam")\
        .getOrCreate()
    
    # Define Columns
    originColumns = ["win","b1","b2","b3","b4","b5","b6","b7","b8","b9","b10","p1","p1p","p2","p2p","p3","p3p"]
    labelColumn = "p3"
    stringColumns = ["p1p", "p2p", "p3p"]
    indexColumns = [column+"_i" for column in stringColumns]
    vectorColumns = [column+"_v" for column in indexColumns]
    featureColumns = []
    for column in originColumns:
        if column != labelColumn and not column in stringColumns:
            featureColumns.append(column)
    for column in vectorColumns:
        featureColumns.append(column)
    
    # Load DataFrame
    data = spark.read.load("data/3187/yzh/t2.csv",format="csv",sep=',',inferSchema="true",header="false")
    data = data.toDF(*originColumns)

    # Turn string to index
    indexers = [StringIndexer(inputCol=column,outputCol=column+"_i").fit(data) for column in stringColumns]
    data = Pipeline(stages=indexers).fit(data).transform(data)
    # Turn index to vector
    encoder = OneHotEncoderEstimator(inputCols=indexColumns,outputCols=vectorColumns)
    data = encoder.fit(data).transform(data)
    # Combine vectors to one
    assembler = VectorAssembler(inputCols=featureColumns,outputCol="features")
    data = assembler.transform(data)

    # Split data into train and test
    rSplit = data.randomSplit([0.8,0.2], 100)
    dataTrain = rSplit[0].select("features", labelColumn)
    dataTest = rSplit[1].select("features", labelColumn)

    # Creat, train, fit model
    lr = LogisticRegression(maxIter=20,regParam=0.01,probabilityCol="probability")
    model = lr.fit(dataTrain.withColumnRenamed(labelColumn, "label"))
    result = model.transform(dataTest).select(labelColumn, "prediction", "probability").collect()
    
    # Check, show result
    counter = [0,0]
    for row in result:
        counter[0] += 1
        if row[labelColumn] == row.prediction:
            counter[1] += 1
    print("----- Mission Complite -----")
    print(f"Predicted {counter[0]} items, and {counter[1]} are correct.")
    print(f"Correct rate is {round(counter[1]/counter[0]*10000)/100}%")
    print("")

    # Exit
    exit()

    # Learn a LogisticRegression model. This uses the parameters stored in lr.
    model1 = lr.fit(dataTraining)

    # Since model1 is a Model (i.e., a transformer produced by an Estimator),
    # we can view the parameters it used during fit().
    # This prints the parameter (name: value) pairs, where names are unique IDs for this
    # LogisticRegression instance.
    print("Model 1 was fit using parameters: ")
    print(model1.extractParamMap())

    # We may alternatively specify parameters using a Python dictionary as a paramMap
    paramMap = {lr.maxIter: 20}
    paramMap[lr.maxIter] = 30  # Specify 1 Param, overwriting the original maxIter.
    paramMap.update({lr.regParam: 0.1, lr.threshold: 0.55})  # Specify multiple Params.

    # You can combine paramMaps, which are python dictionaries.
    paramMap2 = {lr.probabilityCol: "myProbability"}  # Change output column name
    paramMapCombined = paramMap.copy()
    paramMapCombined.update(paramMap2)

    # Now learn a new model using the paramMapCombined parameters.
    # paramMapCombined overrides all parameters set earlier via lr.set* methods.
    model2 = lr.fit(training, paramMapCombined)
    print("Model 2 was fit using parameters: ")
    print(model2.extractParamMap())

    # Prepare test data
    test = spark.createDataFrame([
        (1.0, Vectors.dense([-1.0, 1.5, 1.3])),
        (0.0, Vectors.dense([3.0, 2.0, -0.1])),
        (1.0, Vectors.dense([0.0, 2.2, -1.5]))], ["label", "features"])

    # Make predictions on test data using the Transformer.transform() method.
    # LogisticRegression.transform will only use the 'features' column.
    # Note that model2.transform() outputs a "myProbability" column instead of the usual
    # 'probability' column since we renamed the lr.probabilityCol parameter previously.
    prediction = model2.transform(test)
    result = prediction.select("features", "label", "myProbability", "prediction") \
        .collect()

    for row in result:
        print("features=%s, label=%s -> prob=%s, prediction=%s"
              % (row.features, row.label, row.myProbability, row.prediction))
    # $example off$

    spark.stop()
