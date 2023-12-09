# Open puzzle input and store data [PART 1]
def recordDataPart1():
    with open ('input', 'r') as f:
        lines = []
        for line in f:
            # print(line.strip().split())
            cleanLine = line.strip()
            
            firstNumber = None
            secondNumber = None
            
            # Search line in forward order
            for char in cleanLine:
                stopLoop = char.isnumeric()
                if stopLoop:
                    firstNumber = char
                    break
                
            # Search line in reverse order
            for char in reversed(cleanLine):
                stopLoop = char.isnumeric()
                if stopLoop:
                    secondNumber = char
                    break
            
            lines.append(int(firstNumber + secondNumber))

    return lines

# Open puzzle input and store data [PART 2]
def recordDataPart2():
    with open ('input', 'r') as f:
        lines = []
        for line in f:
            # print(line.strip().split())
            cleanLine = line.strip()
            
            firstNumber = None
            secondNumber = None
            
            # Search line in forward order
            firstNumber = searchNumber(cleanLine)
                
            # Search line in reverse order
            secondNumber = searchNumber((reversed(cleanLine)))
            
            lines.append(int(str(firstNumber) + str(secondNumber)))

    return lines


# Search for written number [PART 2]
def searchNumber(input):
    numbers = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    # luckyNumber = 0
    parsedString = ""
    
    # Search line in forward order
    for char in input:
        # Exit out of loop if int number is found
        if (char.isnumeric()):
            return int(char)
        
        # Build string
        parsedString = parsedString + char
        
        # Check if string contains written number
        for k, v in numbers.items():
            if k in parsedString:
                return v
            if k in parsedString[::-1]:
                return v

# Algorithim for determining sum of calibration values
def sumCalibratedValues(calibratedValues):
    sumOfVals = 0
    
    for val in calibratedValues:
        sumOfVals = sumOfVals + val

    return sumOfVals

# Main Loop
def main():
    outputPart1  = "Puzzle answer for Part 1: "
    outputPart2  = "Puzzle answer for Part 2: "
    calibratedValuesPart1 = recordDataPart1()
    calibratedValuesPart2 = recordDataPart2()
    
    calibratedValuePart1 = sumCalibratedValues(calibratedValuesPart1)
    calibratedValuePart2 = sumCalibratedValues(calibratedValuesPart2)

    print(outputPart1, calibratedValuePart1)
    print(outputPart2, calibratedValuePart2)

if __name__ == "__main__":
    main()