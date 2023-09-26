import serial
import time
import csv

ser = serial.Serial('/dev/tty.usbserial-DT03KIUS', 115200)

#start_time=time.time()
#while (time.time() - start_time < 30):
while True:
    #with open("FeatherweightPackets","rb") as d:
        #data=d.readline()
    data = ser.readline()
    print(data)
    
    stat = bytes("@ GPS_STAT", encoding="utf-8")

    #if the serial data starts with "@ GPS_STAT", write the line to a new FilteredData file
    if (data.startswith(stat)):
        with open("FilteredData", "r+") as fd:
            fd.write(str(data) + '\n')

    #read from the filtered data and write the relevant data to a CSV file
    with open("FilteredData", "r") as fd2:
        line=fd2.readline()
        time = line[27:40]

        altindex = line.index('Alt')
        latindex = line.index('lt')
        longindex = line.index('ln')
        velindex = line.index('Vel')

        alt = line[altindex + 4: latindex - 1]
        lat = line[latindex + 3: longindex - 1]
        long = line[longindex + 3: velindex - 1]
        hvel = line[velindex + 4: velindex + 9]
        hhead = line[velindex + 10:velindex + 14]
        uvel = line[velindex + 15: velindex + 20]
        
        #creates a csv file for the parsed data
        with open('data.csv', mode='w') as csvfile:
            #sets the column headers
            fieldnames = ['Time', 'Altitude', 'Latitude', 'Longitude', 'Horizontal Velocity', 'Horizontal Heading', 'Upward Velocity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            #writes the rows with the relevant data
            writer.writerow({'Time':time, 'Altitude':alt, 'Latitude':lat, 'Longitude':long, 'Horizontal Velocity':hvel, 'Horizontal Heading':hhead, 'Upward Velocity':uvel})