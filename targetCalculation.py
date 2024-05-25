import serial as s
import time as t

ser = s.Serial('/dev/cu.usbmodem54E20242861', 115200)  # check your com port
out = s.Serial('/dev/cu.usbserial-14310', 9600)

baseData = []
count = 0

while count < 8:
    data = ser.readline()
    data = data.decode()
    x = data.split("\t")
    x.pop(0)
    x[-1] = x[-1].removesuffix("\r\n")
    x = list(map(int, x))
    baseData.append(x)
    count += 1

print("base data: ")
print(baseData)

while True:
    ser.readline()
    currentData = []
    for i in range(8):
        data = ser.readline()
        data = data.decode()
        y = data.split("\t")
        y.pop(0)
        y[7] = y[7].removesuffix("\r\n")
        y = list(map(int, y))
        currentData.append(y)
        
    print("current data: ")
    result = [[0,0,0,0,0,0,0,0], 
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0]]
    result2 = [[0,0,0,0,0,0,0,0], 
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0],
              [0,0,0,0,0,0,0,0]]
    for i in range(len(baseData)):
        for j in range(len(baseData[0])):
            kissa = baseData[i][j] - currentData[i][j]
            result[i][j] = kissa
            if 500 > kissa > 250:
                result2[i][j] = 1
            if 750 > kissa >= 500:
                result2[i][j] = 2
            if 1000 > kissa >= 750:
                result2[i][j] = 3
            if 1250 > kissa >= 1000:
                result2[i][j] = 4
            if 1500 > kissa >= 1250:
                result2[i][j] = 5
            if 1750 > kissa >= 1500:
                result2[i][j] = 6
            if  kissa >= 1750:
                result2[i][j] = 7
            
    #Finding the target
    sum = 0
    targetRow = 4
    maxSumRow = 0
    targetColumn = 4
    maxSumColumn = 0

    for i in range(8):
        for j in range(8):
            sum += result2[i][j]
        if sum > maxSumRow:
            maxSumRow = sum
            targetRow = i
        sum = 0
    
    for i in range(8):
        for j in range(8):
            sum += result2[j][i]
        if sum > maxSumColumn:
            maxSumColumn = sum
            targetColumn = i
        sum = 0


    # Printing the result
    print("Subtraction of two matrix")
    for row in result:
        for element in row:
            print(element, end=" ")
        print()

    print("kissa taulukko")
    for row in result2:
        for element in row:
            print(element, end=" ")
        print()

    print("target point", targetRow, " + ", targetColumn)

    currentDegreeC = 32.5
    targetColumnDegree = targetColumn * 8.125
    turningDegreeC = targetColumnDegree - currentDegreeC
    turningStepC = turningDegreeC / 1.8
    currentDegreeC = targetColumnDegree

    currentDegreeR = 32.5
    targetRowDegree = targetRow * 8.125
    turningDegreeR = targetRowDegree - currentDegreeR
    turningStepR = turningDegreeR / 0.6
    currentDegreeR = targetRowDegree

    joo = str( int(round(turningStepC)) ) + "," + str( int(round(turningStepR)) ) + "\n"
    print(joo)

    out.write(bytes(joo.encode()))

