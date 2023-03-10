from django.shortcuts import render

# Create your views here.

import findspark
import random
from pyspark.mllib.recommendation import *
from operator import *
from collections import defaultdict
from pyspark import SparkContext, SparkConf




def home(request):
    userId=request.GET.get('userId')
    # Import libraries
    findspark.init()


    # Initialize Spark Context
    
    spark = SparkContext.getOrCreate()
    spark.stop()
    spark = SparkContext('local','Recommender')
   

    # Importer les fichiers de tests dans Les variables RDD

    artistData = spark.textFile("C:\\Users\\Oussama\\Downloads\\Music-recommender-with-Spark-main\\Music-recommender-with-Spark-main\static\\artist_data_small.txt")
    artistAlias = spark.textFile("C:\\Users\\Oussama\\Downloads\\Music-recommender-with-Spark-main\\Music-recommender-with-Spark-main\static\\artist_alias_small.txt")
    userArtistData = spark.textFile("C:\\Users\\Oussama\\Downloads\\Music-recommender-with-Spark-main\\Music-recommender-with-Spark-main\static\\user_artist_data_small.txt")

    # Split a sequence into seperate entities and store as int

    artistData= artistData.map(lambda s:(int(s.split("\t")[0]),s.split("\t")[1]))
    userArtistData = userArtistData.map(lambda s:(int(s.split(" ")[0]),int(s.split(" ")[1]),int(s.split(" ")[2])))

    # Creation d'un dictionnaire du dataset artist alias 

    artistAliasDictionary = {}
    dataValue = artistAlias.map(lambda s:(int(s.split("\t")[0]),int(s.split("\t")[1])))
    for temp in dataValue.collect():
        artistAliasDictionary[temp[0]] = temp[1]

    # If artistid exists, replace with artistsid from artistAlias, else retain original
    userArtistData = userArtistData.map(lambda x: (x[0], 
    artistAliasDictionary[x[1]] if x[1] in artistAliasDictionary else x[1], x[2]))

    #Créer un RDD composé d'objets 'userid' et 'playcount' du tuple d'origine   
    # userSum = userArtistData.map(lambda x:(x[0],x[2]))
    # playCount1 = userSum.map(lambda x: (x[0],x[1])).reduceByKey(lambda a,b : a+b)
    # playCount2 = userSum.map(lambda x: (x[0],1)).reduceByKey(lambda a,b:a+b)
    # playSumAndCount = playCount1.leftOuterJoin(playCount2)


    # # Compter les instances par clé et stocker dans la variable de diffusion

    # playSumAndCount = playSumAndCount.map(lambda x: (x[0],x[1][0],int(x[1][0]/x[1][1])))

    # # Compute and display users with the highest playcount along with their mean playcount across artists
    # # YOUR CODE GOES HERE

    # TopThree = playSumAndCount.top(3,key=lambda x: x[1])
    # for i in TopThree:
    #     print('User '+str(i[0])+' has a total play count of '+str(i[1])+' and a mean play count of '+str(i[2])+'.')


    # Split the 'userArtistData' dataset into training, validation and test datasets. Store in cache for frequent access
    # YOUR CODE GOES HERE

    trainData, validationData, testData = userArtistData.randomSplit((0.4,0.4,0.2),seed=13)
    trainData.cache()
    validationData.cache()
    testData.cache()

    # Display the first 3 records of each dataset followed by the total count of records for each datasets
    # YOUR CODE GOES HERE


    print(trainData.take(3))
    print(validationData.take(3))
    print(testData.take(3))
    print(trainData.count())
    print(validationData.count())
    print(testData.count())

    # rankList = [2,10,20]
    # for rank in rankList:

    #     model = ALS.trainImplicit(trainData, rank , seed=345)
        # modelEval(model,validationData)
        # 

    # Find the top 5 artists for a particular user and list their names
    # YOUR CODE GOES HERE*
    print("eeeee")
    bestModel = ALS.trainImplicit(trainData, rank=10, seed=345)

    topFive = []
    print("dddd")
    if userId : 
        print("ccccccccc")
        print(userId)
        TopFive = bestModel.recommendProducts(int(userId),5)
        for item in range(0,5):
            topFive.append(artistData.filter(lambda x:x[0] == TopFive[item][1]).collect()[0][1])
            print("aaaaa",item)
    

    context={"topFiveList":topFive}
    return render(request,'index.html',context)


    