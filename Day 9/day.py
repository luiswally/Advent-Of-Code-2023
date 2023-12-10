# Open puzzle input and store data
def recordData():
    with open ('input', 'r') as f:
        winsList = []
        rollsList = []
        for line in f:
            cleanLine = line.strip()
            card = cleanLine.split(':')
            numbers = card[1].split('|')
            winners = numbers[0].strip().split()
            rolls = numbers[1].strip().split()

            winners = [int(x) for x in winners]
            rolls = [int(x) for x in rolls]

            winsList.append(winners)
            rollsList.append(rolls)

    return winsList, rollsList

# Algorithim for determining points gained in a game
def countPoints(win, roll):
    # # rudimentary piecewise solution
    # points = 0
    # for number in roll:
    #     if number in win:
    #         if points == 0:
    #             points = 1
    #         else:
    #             points = 2 * points            

    # power solution
    counter = -1
    for number in roll:
        if number in win:
            counter += 1

    if counter > -1:
        points = 2 ** counter
    else:
        points = 0

    return points

# Algorithim for copies of cards gained in a game
def countCopies(win, roll):      
    count = 0
    for number in roll:
        if number in win:
            count += 1

    return count

# Pipeline for determining all points gained in each card [PART 1]
def sumAllPoints(winsList, rollsList):
    points = 0
    for card, roll in enumerate(rollsList):
        win = winsList[card]
        pointsGained = countPoints(win, roll)
        
        points += pointsGained

    return points

# Pipeline for determining all scratch card instances [PART 2]
def sumScratchCards(winsList, rollsList):
    cardInstances = [1] * len(rollsList)

    for card, roll in enumerate(rollsList):
        thisCardInstanceCount = cardInstances[card]
        win = winsList[card]
        cardCopies = countCopies(win, roll)
        if cardCopies > 0:
            start = card + 1
            end = card + cardCopies
            
            for cardToCopy in range(start, end+1):
                cardInstances[cardToCopy] += thisCardInstanceCount

    return sum(cardInstances)

# Main Loop through 
def main():
    # constants
    outputPart1  = "Puzzle answer for Part 1: "
    outputPart2  = "Puzzle answer for Part 2: "
    
    # load data
    winsList, rollsList = recordData()
    
    # working area - clean up after solution
    
    # solution routines called
    solPart1 = sumAllPoints(winsList, rollsList)
    solPart2 = sumScratchCards(winsList, rollsList)
    
    print(outputPart1, solPart1)
    print(outputPart2, solPart2)


if __name__ == "__main__":
    main()