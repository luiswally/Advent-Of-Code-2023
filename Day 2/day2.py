# Open puzzle input and store data
def recordData():
    with open ('input', 'r') as f:
        lines = []
        for line in f:
            cleanLine = line.strip()
            
            gameSet = cleanLine.split(':')
            
            games = gameSet[0].split(' ')
            gameNumber = int(games[1].strip())
            
            allSets = gameSet[1].strip()
            
            rolls = parseGames(allSets)
            
            game = [gameNumber] + rolls
            
            lines.append(game)

    return lines

# Convert input into usable data strucuture
def parseGames(allSets):
    gameRolls = []
    
    # Get unfiltered sets
    sets = allSets.split(';')
    for set in sets:
        setRolls = [0, 0, 0] # [R G B]
        rolls = set.split(',')
        for roll in rolls:
            pair = roll.strip().split(' ')
            
            cubeCount = int(pair[0])
            cubeColor = pair[1]
            if 'red' in cubeColor:
                setRolls[0] = cubeCount
            elif 'green' in cubeColor:
                setRolls[1] = cubeCount
            elif 'blue' in cubeColor:
                setRolls[2] = cubeCount
        
        gameRolls.append(setRolls)
    
    return gameRolls

# Playble condition identifier
def playableCondition(set):
    cubes = [12, 13, 14] # limited by cubes to play with
    
    redPlayble = set[0] <= cubes[0]
    greenPlayble = set[1] <= cubes[1]
    bluePlayble = set[2] <= cubes[2]
    
    return redPlayble * greenPlayble * bluePlayble


# Algorithim for determining sum of playable game indices
def sumPlayableGameIndexes(games):
    sum = 0
    
    for game in games:
        playable = True
        index = game[0]
        sets = game[1::]
        for set in sets:
            playable = playableCondition(set)
            if not playableCondition(set):
                break
        if playable:
            sum = sum + index

    return sum

# Algorithim for determining minimum count of cubes per game
def minPower(sets):
    cubes = [0, 0, 0]
    
    for set in sets:
        red = set[0]
        green = set[1]
        blue = set[2]
        
        if red >= cubes[0]:
            cubes[0] = red
        if green >= cubes[1]:
            cubes[1] = green
        if blue >= cubes[2]:
            cubes[2] = blue

    return cubes[0] * cubes[1] * cubes[2]

# Algorithim for determining sum of playable game indices
def sumMinPowers(games):
    sum = 0
    
    for game in games:
        sets = game[1::]
        sum = sum + minPower(sets)
    return sum

# Main Loop
def main():
    outputPart1  = "Puzzle answer for Part 1: "
    outputPart2  = "Puzzle answer for Part 2: "
    games = recordData()
    
    sumPlayableIndexes = sumPlayableGameIndexes(games)
    
    print(outputPart1, sumPlayableIndexes)
    print(outputPart2, sumMinPowers(games))

if __name__ == "__main__":
    main()