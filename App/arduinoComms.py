import serial
import time
import datetime
import math


# initialize variables for storing
id = 10         # this id needs to be unique to each machine
day = ''
temp = 0    
humidity = 0
waterheight = 0
waterlevel = 0
waterproduced = 0
power = 0
tds = 0

# these three values depend on the operating voltage of the AWG and the dimensions of the water storage container (measurements in centimeters)
voltage = 120
containerheight = 12.7
containerRadius = 5.08

def main():
    global id, day, temp, humidity, waterheight, waterlevel, waterproduced, power, tds, voltage
    collectData()
    saveData()

def readFromArduino(serialPort):
    # this function will collect data from the sensors through the serial communications of each arduino
    global id, day, temp, humidity, waterheight, waterlevel, waterproduced, power, tds, voltage
    timeout = 5
    startTime = time.time()
    try:
        while (time.time() - startTime) < timeout:
            line = serialPort.readline().decode('utf-8').strip()
            parts = line.split(" ")
            if (parts[0] == "th"):
                temp = float(parts[1])
                humidity = float(parts[2])
            elif (parts[0] == "tds"):
                tds = int(parts[1])
                if (tds > 1000):
                    tds = 1000
                if (tds < 10):
                    tds = 0
            elif (parts[0] == "water"):
                waterheight = containerheight - float(parts[1])
            elif (parts[0] == "current"):
                # calculates the power consumption in KWH of the most recent 30 minute interval
                power = (3/6) * ((float(parts[1]) * voltage) / 1000)

            print(f'Received from Arduino {serialPort.port}: {line}')
    except KeyboardInterrupt:
        pass

def saveData():
    global id, day, temp, humidity, waterheight, waterlevel, waterproduced, power, tds

    # get a new timestamp and use the data collected from the sensors to populate the file
    generateDay()
    try:
        data = open("sensorData.txt", "r")

        # (old data exists)
        # create a new sensor data file by referencing past data when applicable (power, water level/produced)
        # (When there is a new day we will need to reference the old water level in order to find the new water produced)

        timeString = data.readline()
        dayFromString = timeParser(timeString)
        if (dayFromString < datetime.date.today()):
            # we are now collecting data on a new day so we need to reset our power/water produced
            data.readline() # move past ID line
            data.readline() # move past temp line
            data.readline() # move past humidity line

            # find water produced
            oldwaterheight = float(data.readline())
            findWaterLevel()
            if (waterheight <= oldwaterheight):
                waterproduced = 0
            else:
                # do math to figure out new production!!!
                findWaterProduced(waterheight, oldwaterheight)

            # write values back to file
            data.close()
            data = open("sensorData.txt", "w")
            data.write(day + "\n" + str(id) + "\n" + str(temp) + "\n" + str(humidity) + "\n" + str(waterheight) + "\n" + str(waterlevel) + "\n" + str(waterproduced) + "\n" + str(power) +"\n" + str(tds))


        else:
            # we are collecting data for the same day so we need to add to water/power values
            data.readline() # move past ID line
            data.readline() # move past temp line
            data.readline() # move past humidity line

            # find water produced
            oldwaterheight = float(data.readline())
            data.readline() # move past waterlevel line
            oldwaterproduced = float(data.readline())
            findWaterLevel()
            if (waterheight <= oldwaterheight):
                waterproduced = oldwaterproduced
            else:
                # do math to figure out new production!!!
                findWaterProduced(waterheight, oldwaterheight)
                waterproduced += oldwaterproduced 
            
            # find power produced
            oldpower = float(data.readline())
            power += oldpower

            # write values back to file
            data.close()
            data = open("sensorData.txt", "w")
            data.write(day + "\n" + str(id) + "\n" + str(temp) + "\n" + str(humidity) + "\n" + str(waterheight) + "\n" + str(waterlevel) + "\n" + str(waterproduced) + "\n" + str(power) +"\n" + str(tds))


    except FileNotFoundError:
        # HARD RESET (old data does not exist)
        # create a new sensor data file without referencing past data

        data = open("sensorData.txt", "w")

        findWaterLevel()
        waterproduced = 0
        data.write(day + "\n" + str(id) + "\n" + str(temp) + "\n" + str(humidity) + "\n" + str(waterheight) + "\n" + str(waterlevel) + "\n" + str(waterproduced) + "\n" + str(power) +"\n" + str(tds))
        data.close()

def findWaterLevel():
    # calculates the total volume of liquid in a cylindrical tank using its radius and fill amount
    global containerRadius, waterlevel, waterheight
    waterlevel = (waterheight * pow(containerRadius, 2) * math.pi) / 1000

def findWaterProduced(newheight, oldheight):
    # calculates the volume of liquid that was produced in a cylindrical tank using its radius and fill amount
    global containerRadius, waterproduced

    waterproduced = ((newheight - oldheight) * pow(containerRadius, 2) * math.pi) / 1000
    if (waterproduced < 0.01):
        waterproduced = 0

def generateDay():
    global day
    day = datetime.date.today().strftime("%Y %m %d")

def timeParser(line):
    dayParts = line.split(" ")
    return datetime.date(int(dayParts[0]), int(dayParts[1]), int(dayParts[2]))



def collectData():
    # Replace these with the actual serial port names for your Arduinos
    arduinoPorts = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2']#, '/dev/ttyACM3']

    # Open connections to Arduino ports
    arduinoSerialPorts = [serial.Serial(port, 9600) for port in arduinoPorts]

    try:
        # Switch between Arduino inputs (you can modify this loop based on your specific requirements)
        for arduinoPort in arduinoSerialPorts:
            print(f"Switching to Arduino on port {arduinoPort.port}")
            readFromArduino(arduinoPort)
            print(f"Finished gathering data from Arduino {arduinoPort.port}")
            time.sleep(2)  # Add a delay if needed

    except KeyboardInterrupt:
        pass

    finally:
        # Close all serial ports when done
        for arduino_port in arduinoSerialPorts:
            arduino_port.close()



if __name__ == "__main__":
    main()
