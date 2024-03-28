from pymongo import MongoClient
import datetime
import json

# initialize collection
collection = ''


# initialize variables for datapack
id = 10             # this id needs to be unique to each machine
timestamp = ''
temp = 0    
humidity = 0
waterlevel = 0
waterproduced = 0
power = 0
tds = 0

dataPack = {}

def main():

    if (retrieveSensorData() < 0): return

    connectDB()

    generateTime()

    createDataPack()

    # insert the datapack into the collection in the database
    result = collection.insert_one(dataPack)
    print(result)


def connectDB():
    global collection
    # connect to database (client url will need to be replaced with a new one that links to the current mongodb database)
    client = MongoClient('mongodb+srv://Proefey:0UPYpvGmo21iyI5l@teamflow.u4jpeoh.mongodb.net/TeamFlow?retryWrites=true&w=majority')
    
    # set database client and collection (db and collection will need to be the corresponding names in the current mongodb database)
    db = client['TeamFlow']
    collection = db['DataPack']

def createDataPack():
    # format the datapack
    global dataPack, id, timestamp, temp, humidity, waterlevel, waterproduced, power, tds
    dataPack = {
        'machineID': id,
        'timestamp': timestamp,
        'temp': temp,
        'humidity': humidity,
        'waterlevel': waterlevel,
        'waterproduced': waterproduced,
        'power': power,
        'tds': tds
    }

def retrieveSensorData():
    # this function will move past irrelevant data in the sensorData.txt file and retrieve the relevant values in the correct format for sending to the database
    global id, temp, humidity, waterlevel, waterproduced, power, tds
    try:
        data = open("sensorData.txt", "r")

        data.readline() # move past day

        id = int(data.readline())
        temp = float(data.readline())
        humidity = float(data.readline())

        data.readline() # move past waterheight
        waterlevel = "{:.2f}".format(float(data.readline()))
        waterproduced = "{:.2f}".format(float(data.readline()))
        power = "{:.2f}".format(float(data.readline()))
        tds = float(data.readline())
        return 0


    except FileNotFoundError:
        print("Data file not found")
        return -1


def generateTime():
    global timestamp
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    json.dumps(timestamp.isoformat())



if __name__ == "__main__":
    main()