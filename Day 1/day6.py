# Open puzzle input and store data
def recordData():
    with open ('input', 'r') as f:
        lines = []
        for line in f:
            # print(line.strip().split())
            lines.append(line.strip().split())

    time = [int(x) for x in lines[0][1::]]
    distances = [int(x) for x in lines[1][1::]]

    return time, distances

# Algorithim for determining win cases
def countWinCases(time, distance):
    timeToAccelerate = list(range(1, time+1, 1))
    timeToTravel = []
    
    for t in timeToAccelerate:
        timeLeft = time - t
        timeToTravel.append(timeLeft)
    
    # Determine distance traveled under each condition (wait times)
    distanceTraveled = [t1 * t2 for t1, t2 in zip(timeToAccelerate, timeToTravel)]

    # Determine list of wait times based off distance traveled
    winList = [1 if dT >= distance else 0 for dT in distanceTraveled]

    countWins = sum(winList)

    return countWins

# Main Loop through 
def main():
    time, distances = recordData()
# Section for Part Two [turn off for Part 1]
    # Concat elements into one
    revisedTime = "".join(str(x) for x in time)
    revisedDistances = "".join(str(x) for x in distances)
    
    # Revert to array
    time = [int(revisedTime)]
    distances = [int(revisedDistances)]
# Section for Part Two [turn off for Part 1]
    
    winFactor = 1
    for race, t in enumerate(time):
        Time = t
        Distance = distances[race]

        winFactor = winFactor * countWinCases(Time, Distance)

    print(winFactor)

if __name__ == "__main__":
    main()