from __future__ import print_function

from time import time

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.externals import joblib
import pymysql, glob, os, csv

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'hacareem'

def getData(file):
    data = dict()

    print("Reading file: " + file)
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        for features in reader:
            if features[0] not in data.keys() :
                data[features[0]] = dict()
                data[features[0]]["data"] = []
                data[features[0]]["target"] = []
            data[features[0]]["data"].append([int(features[2]), float(features[4]), float(features[5])])
            data[features[0]]["target"].append(features[10])

    return data

def firstTraining():
    data = getData("C:\\Users\\draza\\Downloads\\hacareem-khi-master\\problem3\\large2.csv")

    print("%d users" % len(data))
    print()

    for key in data:
        t0 = time()
        if len(data[key]["data"]) < 3 or len(set(data[key]["target"])) < 2:
            continue
        X_train, X_test, y_train, y_test = train_test_split(data[key]["data"], data[key]["target"], test_size=0.33,
                                                            random_state=42)
        clf = SVC()
        clf.fit(X_train, y_train)
        print("done training in %0.3fs" % (time() - t0))
        y_score = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_score)
        if accuracy > 0.49:
            print("accuracy is %0.3f " % accuracy)
            clf2 = SVC()
            clf2.fit(data[key]["data"], data[key]["target"])
            joblib.dump(clf2, key + '.pkl')
        print()

def iterativeTraining():
    userIds = getAllUserIds()

    for userId in userIds:
        data = getTrainingData(userId)
        t0 = time()
        if len(data["data"]) < 3 or len(set(data["target"])) < 2:
            continue
        X_train, X_test, y_train, y_test = train_test_split(data["data"], data["target"], test_size=0.33,
                                                            random_state=42)
        clf = SVC()
        clf.fit(X_train, y_train)
        print("done training in %0.3fs" % (time() - t0))
        y_score = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_score)
        if accuracy > 0.49:
            print("accuracy is %0.3f " % accuracy)
            clf2 = SVC()
            clf2.fit(data["data"], data["target"])
            joblib.dump(clf2, userId + '.pkl')
        print()

def predict(userId, pickTime, pickLat, pickLong):
    modelsDict = dict()
    modelsPath = "C:\\Users\\draza\\PycharmProjects\\HaCareem\\"
    os.chdir(modelsPath)
    for file in glob.glob("*.pkl"):
        modelsDict[file[:-4]] = os.path.join(modelsPath, file)
    # print(modelsDict)

    t0 = time()
    outputList = []
    featureList = [pickTime, pickLat, pickLong]
    if userId in modelsDict:
        clf = joblib.load(modelsDict[userId])
        prediction = clf.predict([featureList])[0]
    else:
        prediction = getPredictions(userId, pickTime, pickLat, pickLong)

    outputList.append(prediction)

    print("prediction time %0.3fms" % ((time() - t0) * 1000.0))

    return outputList

def getPredictions(userId, pickTime, pickLat, pickLong):
    outputList = []
    myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database)
    cur = myConnection.cursor()
    cur.execute( "SELECT drop_off_geohash, COUNT(1) CNT FROM hacareem.trips WHERE user_id = \'" + userId + "\' and ((pick_up_lat = \'" + str(pickLat) + "\' and pick_up_lng = \'" + str(pickLong) + "\') or ((pick_up_time - 3600) < \'" + str(pickTime) + "\' and (pick_up_time + 3600) > \'" + str(pickTime) + "\')) GROUP BY drop_off_geohash ORDER BY COUNT(1) DESC" )
    for dropHash, CNT in cur.fetchall() :
        outputList.append(dropHash)
    myConnection.close()
    return outputList

def getTrainingData(userId):
    myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database)
    cur = myConnection.cursor()
    cur.execute( "SELECT pick_up_time, pick_up_lat, pick_up_lng, drop_off_geohash FROM hacareem.trips WHERE user_id = " + userId )
    data = dict()
    data["data"] = []
    data["target"] = []
    for pickTime, pickLat, pickLong, dropHash in cur.fetchall() :
        data["data"].append([pickTime, pickLat, pickLong])
        data["target"].append(dropHash)
    myConnection.close()

    return data


def getAllUserIds():
    myConnection = pymysql.connect(host=hostname, user=username, passwd=password, db=database)
    cur = myConnection.cursor()
    cur.execute("SELECT DISTINCT user_id FROM hacareem.trips")
    userIds = set()
    for userId in cur.fetchall():
        userIds.add(userId)
    myConnection.close()

    return userIds


if __name__ == "__main__":


    # firstTraining()

    totalTime = 0.0
    totalRecords = 0
    with open("C:\\Users\\draza\\Downloads\\hacareem-khi-master\\problem3\\large2.csv") as csvfile:
        reader = csv.reader(csvfile)
        for features in reader:
            totalRecords += 1
            t0 = time()
            predict(features[0], int(features[2]), float(features[4]), float(features[5]))
            totalTime += (time() - t0) * 1000.0
    print("average predict time %0.3fms" % (totalTime / totalRecords))

    print()