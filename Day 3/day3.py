# Open puzzle input and store data
def recordData():
    with open ('input', 'r') as f:
        lines = []
        for line in f:
            input = []
            for char in line.strip():
                input.append(char)
            lines.append(input)

    return lines

# Record all numbers and their corresponding indices
def findNumberAndIndex(active):
    numberList = [] # [ [[number, colStart, colEnd]], ... ]
    start = 0
    currentNumber = ""
    for index, char in enumerate(active):
        if char.isnumeric() and index == len(active) - 1 and currentNumber=="":
            start = index
            currentNumber = currentNumber + char
            number = int(currentNumber)
            numberList.append([number, start, len(active) - 1])
        elif char.isnumeric() and currentNumber=="":
            start = index
            currentNumber = currentNumber + char
        elif char.isnumeric() and index == len(active) - 1 and currentNumber!="":
            currentNumber = currentNumber + char
            number = int(currentNumber)
            numberList.append([number, start, len(active) - 1])
        elif char.isnumeric() and currentNumber!="":
            currentNumber = currentNumber + char
        elif not char.isnumeric() and currentNumber!="":
            number = int(currentNumber)
            numberList.append([number, start, index - 1])
            start = 0
            currentNumber = ""

    return numberList


# Determine if a symbol is present [PART 1 ONLY]
def symbolPresent(segment):
    record = False
    
    for char in segment:
        if (not char.isnumeric()) and (not '.' in char):
            record = True

    return record

# Find gear symbol
def findGearSymbol(active):
    gearList = [] # [ col, ... ]
    for index, char in enumerate(active):
        if '*' in char:
            gearList.append(index)

    return gearList

# Count numbers surrounding potential gears
def countNumbers(power, start, end):
    numberList = []
    # Delete numbers below start
    indexDeleteStart = -1
    for index, powerData in enumerate(power):
        powerEnd = powerData[2]
        if powerEnd < start and index >= indexDeleteStart:
            indexDeleteStart = index

    if indexDeleteStart > -1:
        power = power[indexDeleteStart+1:]
    
    # Delete numbers above end
    indexDeleteEnd = -1
    for index, powerData in enumerate(power):
        powerStart = powerData[1]
        if powerStart > end and indexDeleteEnd == -1 :
            indexDeleteEnd = index

    if indexDeleteEnd > -1:
        power = power[:indexDeleteEnd]
    
    for number in power:
        numberList.append(number[0])

    return numberList

# Find gear numbers associated with REAL gears
def findGearNumbers(active, topPower, middlePower, bottomPower):
    gearNumberList = []
    gearSymbols = findGearSymbol(active)
    
    for index in gearSymbols:        
        # refine start/end limits
        if index == 0:
            start = index
            end = index + 1
        elif index == len(active) - 1:
            start = index - 1
            end = index
        else:
            start = index - 1
            end = index + 1
        
        topNumbers = countNumbers(topPower, start, end)
        middleNumbers = countNumbers(middlePower, start, end)
        bottomNumbers = countNumbers(bottomPower, start, end)
        
        allNumbers = topNumbers + middleNumbers + bottomNumbers
        if len(allNumbers) == 2:
            gearNumberList.append(allNumbers)

    return gearNumberList



# Parser for part number
def findPartNumbers(top, active, bottom):
    numberList = [] # [ [[number, colStart, colEnd]], ... ]
    numbers = findNumberAndIndex(active)
    
    
    for number in numbers:
        numberValue = number[0]
        
        # refine start/end limits
        if number[1] == 0:
            start = number[1]
        else:
            start = number[1] - 1
        if number[2] == len(active) - 1:
            end = number[2]
        else:
            end = number[2] + 1

        topSegment = top[start:end+1]
        middleSegment = active[start:end+1]
        bottomSegment = bottom[start:end+1]

        if symbolPresent(topSegment) or symbolPresent(bottomSegment) or symbolPresent(middleSegment):
            numberList.append([numberValue, number[1], number[2]])

    return numberList

# Algorithim for determining sum of ALL part numbers [PART 1 ONLY]
def sumPartNumbers(lines):
    sum = 0
    powerNumberList = []
    
    for row, line in enumerate(lines):
        if row == 0:
            start = row
            middle = row
            end = row + 1
        elif row == len(lines) - 1:
            start = row - 1
            middle = row
            end = row
        else:
            start = row - 1
            middle = row
            end = row + 1
        
        powerNumberList.append(findPartNumbers(lines[start], lines[middle], lines[end]))

    for row in powerNumberList:
        for number in row:
            sum = sum + number[0]

    return powerNumberList, sum

# Algorithim for determining sum of ALL gear part numbers [PART 2 ONLY]
def sumGearNumbers(lines, powerNumberList):
    sum = 0
    gearNumberList = []
    for row, line in enumerate(lines):
        if row == 0:
            start = row
            middle = row
            end = row + 1
            
            topPower = []
            middlePower = powerNumberList[middle]
            bottomPower = powerNumberList[end]
            
        elif row == len(lines) - 1:
            start = row - 1
            middle = row
            end = row
            
            topPower = powerNumberList[start]
            middlePower = powerNumberList[middle]
            bottomPower = []
        else:
            start = row - 1
            middle = row
            end = row + 1
            topPower = powerNumberList[start]
            middlePower = powerNumberList[middle]
            bottomPower = powerNumberList[end]


        gearNumberList.append(findGearNumbers(lines[middle], topPower, middlePower, bottomPower))

    for row in gearNumberList:
        for gear in row:
            sum = sum + gear[0] * gear[1]

    return gearNumberList, sum
        
        
# Main Loop through 
def main():
    outputPart1  = "Puzzle answer for Part 1: "
    outputPart2  = "Puzzle answer for Part 2: "
    lines = recordData()
    
    powerNumberList, solPart1 = sumPartNumbers(lines)
    print(outputPart1, solPart1)
    
    gearNumberList, solPart2 = sumGearNumbers(lines, powerNumberList)
    print(outputPart2, solPart2)
    
if __name__ == "__main__":
    main()