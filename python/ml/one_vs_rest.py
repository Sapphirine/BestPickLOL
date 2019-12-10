from pyspark.ml import Pipeline
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import StringIndexer, OneHotEncoderEstimator, VectorAssembler
from pyspark.ml.classification import LogisticRegression, OneVsRest
from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("EstimatorTransformerParam")\
        .getOrCreate()
    
    # Define Columns
    originColumns = ["win","b1","b2","b3","b4","b5","b6","b7","b8","b9","b10", \
        "p1","p1p","p2","p2p","p3","p3p","p4","p4p","p5","p5p","p6","p6p","p7","p7p","p8","p8p","p9","p9p","p10","p10p"]
    labelColumn = "win"
    stringColumns = ["p1p", "p2p", "p3p", "p4p", "p5p", "p6p", "p7p", "p8p", "p9p", "p10p",]
    indexColumns = [column+"_i" for column in stringColumns]
    vectorColumns = [column+"_v" for column in indexColumns]
    featureColumns = []
    for column in originColumns:
        if column != labelColumn and not column in stringColumns:
            featureColumns.append(column)
    for column in vectorColumns:
        featureColumns.append(column)
    
    # Load DataFrame
    data = spark.read.load("data/3187/yzh/t6.csv",format="csv",sep=',',inferSchema="true",header="false")
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
    rSplit = data.randomSplit([0.97,0.03], 100)
    dataTrain = rSplit[0].select("features", labelColumn)
    dataTest = rSplit[1].select("features", labelColumn)

    # Creat, train, fit model
    lr = LogisticRegression(maxIter=20,regParam=0.01)
    ovr = OneVsRest(classifier=lr)
    model = ovr.fit(dataTrain.withColumnRenamed(labelColumn, "label"))
    result = model.transform(dataTest).select(labelColumn, "prediction").collect()
    
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

    spark.stop()
