# Open puzzle input and store data
def recordData(file):
    with open (file, 'r') as f:
        bigMap = {
            'seeds'                               :   [], # [seed1, seed2, seed3, ...] {int}
            'seed-to-soil'                        :   [],
            'soil-to-fertilizer'                  :   [],
            'fertilizer-to-water'                 :   [],
            'water-to-light'                      :   [],
            'light-to-temperature'                :   [],
            'temperature-to-humidity'             :   [],
            'humidity-to-location'                :   [] # [ [destinationStart, sourceStart, rangeLength], [], [] ] {int} for many entries of different ranges
        }
        currentMap = ''

        for row, line in enumerate(f):
            cleanLine = line.strip()

            if row == 0:
                values = cleanLine.split(':')
                seedNumbersString = values[1].strip().split()
                seedNumbers = [int(x) for x in seedNumbersString]

                currentMap = values[0]
                bigMap.update({currentMap: seedNumbers})
            else:
                rowData = cleanLine.split()
                if rowData:
                    if(not rowData[0].isnumeric()):
                        currentMap = rowData[0]
                    else:
                        thisEntry = [int(x) for x in rowData]
                        
                        # general map update
                        currentEntry = bigMap.get(currentMap)
                        currentEntry.append(thisEntry)
                        bigMap.update({currentMap: currentEntry})

                else:
                    continue

    return bigMap

# Algorithim for determining destination
def findDestination(map, source):
    destination = source # default destination in case not found in map
    
    for entry in map:
        min = entry[1]
        max = min + entry[2] - 1
        
        if source in range(min, max + 1):
             delta = source - min
             destination = entry[0] + delta
             
             return destination
        else:
            continue

    # print("source = ", source, " -> destination = ", destination)
    return destination

# Algorithm for determining location
def findLocation(bigMap, originalSource):
    # assumes the bigMap is sorted as seed->soil->fertilizer->water->light->temperature->humidity->location
    location = 0
    source = originalSource
    
    for mapName, map in bigMap.items():
        # print("This is the map we are working with: ", mapName)
        if 'seeds' in mapName:
            continue
        else:
            source = findDestination(map, source)
    location = source
    
    return location

# Algorithm for determining lower location number [Part 1]
def findMinLocationPart1(bigMap):
    locations = []
    seeds = bigMap.get('seeds')

    for seed in seeds:
        locations.append(findLocation(bigMap, seed))

    return min(locations)

# Algorithm for determining lower location number [Part 2 - TOO SLOW, NEVER USE] O(seed)
def findMinLocationPart2Slow(bigMap):
    locations = []
    seeds = []
    seedPairs = bigMap.get('seeds')
    print("seed pairs are as such: ", seedPairs)

    
    for index, seed in enumerate(seedPairs):
        if not index % 2:
            print('current seed = {', index, "}", seed)
            minSeed = seed
            maxSeed = seed + (seedPairs[index + 1] - 1)
            for realSeed in range(minSeed, maxSeed + 1):
                seeds.append(realSeed)
        else:
            print('range of seed = {', index, "}", seed)
            continue
    
    # print("all the seeds are: ", seeds)

    for count, seed in enumerate(seeds):
        print('seed #', count, '/', len(seeds))
        locations.append(findLocation(bigMap, seed))

    return min(locations)

# Algorithm for determining lower location number [Part 2 - use range overlaps and discard unnecessary portions]
def findMinLocationPart2(bigMap):
    isStandard = False # the desired map merger is exclsuive and only includes REAL SEED
    seedToLocationMap = codex(bigMap)
    
    # use to drive overlap betwween real seeds all location entries
    seedToSeedMap = []
    seedPairs = bigMap.get('seeds')
    for index, seed in enumerate(seedPairs):
        if not index % 2:
            minSeed = seed
            rangeSeed = seedPairs[index + 1]
            seedToSeedMap.append([minSeed, minSeed, rangeSeed])


    # find the seed to location map for ONLY real seed inputs, not overly generalize
    realSeedToLocationMap = mergeMaps(seedToSeedMap, seedToLocationMap, isStandard)
    realSeedToLocationMapSortedByLocation = sorted(realSeedToLocationMap, key = lambda x: x[0])
    
    minLocation = realSeedToLocationMapSortedByLocation[0][0]
    
    return minLocation

# Algorithm for parsing two maps as one, keeps destination from destinationMap, but replaces its source with source from sourceMap and any trailing destinations
def mergeMapsReduction(sourceMap, destinationMap):
    sortedSourceMap = sorted(sourceMap, key = lambda x: x[0]) # sort by intermediate source
    sortedDestinationMap = sorted(destinationMap, key = lambda x: x[1]) # sort by intermediate source
    
    mergedMap = [] # final merger
    
    # keep track of reduced states of sources and destintion maps
    sourceMapReduced = []
    destinationMapReduced = []
    
    # same as above, use to indicatte which to pass forward after first reduction sweep
    wasSourcePartitioned = [False] * len(sourceMap)
    
    # One reduction sweep
    for rowS, sourceEntry in enumerate(sortedSourceMap):
        
        sourceWasPartitioned = False
        for rowD, destEntry in enumerate(sortedDestinationMap):
            if sourceWasPartitioned:
                break #TODO stop this for-loop only
            else:
                overlapEntry = partitionRangeMapEntry(sourceEntry, destEntry)
                if overlapEntry:
                    # Book-keep
                    sourceWasPartitioned = True
                    wasSourcePartitioned[rowS] = sourceWasPartitioned
                    
                    mergedMap.append(overlapEntry) # record overlap
                    
                    # Determine start/end limits to partition ranges
                    startDest = overlapEntry[0]
                    deltaDest = startDest - destEntry[0]
                    startDestSource = destEntry[1] + deltaDest
                    
                    startSourceSource = overlapEntry[1]
                    range = overlapEntry[2]
                    
                    # Create partitions and feed output into reduced maps for next run
                    s1p, s2p, s3p = partitionMapEntry(sourceEntry, startSourceSource, startSourceSource + range - 1)
                    d1p, d2p, d3p = partitionMapEntry(destEntry, startDestSource, startDestSource + range - 1)

                    # Update reduced matrices
                    if s1p:
                        sourceMapReduced.append(s1p)
                    if s3p:
                        sourceMapReduced.append(s3p)
                    if d1p:
                        destinationMapReduced.append(d1p)
                    if d3p:
                        destinationMapReduced.append(d3p)

                    # Stop analyzing the just-partitioned entries in the source and destination map
                    sortedDestinationMap.pop(rowD)


# For the NON partitioned entries (they can't be broken further down) dump back to the reduced matrix for next run
    for rowS, sourceEntry in enumerate(sortedSourceMap):
        if not wasSourcePartitioned[rowS]:
            sourceMapReduced.append(sourceEntry)

    for rowD, destEntry in enumerate(sortedDestinationMap):
        destinationMapReduced.append(destEntry)

    return mergedMap, sourceMapReduced, destinationMapReduced

# Pipeline to merge maps through all iterations
def mergeMaps(sourceMap, destinationMap, isStandard):
    source = sourceMap
    destination = destinationMap
    
    mergedMap = []
    reducedSource = []
    reducedDestination = []
    
    # TODO this while loop may need to compare list exactness, not length
    counter = 0
    while reducedSource != source and reducedDestination != destination:
        if counter == 0:
            thisMergedMap, reducedSource, reducedDestination = mergeMapsReduction(source, destination)
        else:
            source = reducedSource
            destination = reducedDestination
            thisMergedMap, reducedSource, reducedDestination = mergeMapsReduction(source, destination)
        
        if(len(thisMergedMap) != 0):
            for entry in thisMergedMap:
                mergedMap.append(entry)    
    
        counter += 1

    # Maximally reduced entries become a part of the literal translatation since they must correspond
    # This is standard behavior, in the case of REAL SEED map to Location map [part 2], this is not needed
    if isStandard:
        for entry in reducedDestination:
            mergedMap.append(entry)

        for entry in reducedSource:
            mergedMap.append(entry)
    else:
        # reducedDestination should not added to the map since they don't map to REAL SEEDS
        # reducedSource is added to map so that the map has FULL coverage of ALL REAL seeds
        for entry in reducedSource:
            mergedMap.append(entry)
    
    return mergedMap


# Pipeline to get final codex (map)
def codex(bigMap):
    isStandard = True # standard merging occurs for this final map
    # assumes the bigMap is sorted as seed->soil->fertilizer->water->light->temperature->humidity->location
    source = []
    destination = []
        
    for mapName, map in bigMap.items():
        if 'seeds' in mapName:
            continue
        elif 'seed-to-soil' in mapName:
            source = map
        else:
            destination = map
            source = mergeMaps(source, destination, isStandard)
    codex = source    
    
    return codex


# Partition linear sets of ranges and provide the overlap (assuming source is the main range)
def partitionRangeMapEntry(source, destination):
    # useful
    overlap = []
    rangeSource = source[2]
    intStartfromSource = source[0]
    intEndfromSource = intStartfromSource + rangeSource - 1
    
    rangeDest = destination[2]
    intStartfromDest = destination[1]
    intEndfromDest = intStartfromDest + rangeDest - 1

    # parition routine
    if (intEndfromSource < intStartfromDest) or (intStartfromSource > intEndfromDest):
        return overlap
    elif (intStartfromDest <= intStartfromSource and intEndfromDest >= intEndfromSource) or (intStartfromSource <= intStartfromDest and intEndfromSource >= intEndfromDest):
        if intStartfromSource == intStartfromDest and intEndfromSource == intEndfromDest:
            dest = destination[0]
            sorc = source[1]
            ran = rangeSource
            overlap = overlap + [dest, sorc, ran]
            
            return overlap
        elif (intStartfromSource <= intStartfromDest and intEndfromSource >= intEndfromDest):
            leftDelta = intStartfromDest - intStartfromSource

            dest = destination[0]
            sorc = source[1] + leftDelta
            ran = rangeDest
            overlap = overlap + [dest, sorc, ran]
            
            return overlap
        elif (intStartfromDest <= intStartfromSource and intEndfromDest >= intEndfromSource):
            leftDelta = intStartfromSource - intStartfromDest

            dest = destination[0] + leftDelta
            sorc = source[1]
            ran = rangeSource
            overlap = overlap + [dest, sorc, ran]
            
            return overlap
    elif (intStartfromSource <= intStartfromDest and intEndfromSource <= intEndfromDest): #TODO exclude the == inclusion at limits
        leftDelta = intStartfromDest - intStartfromSource
        
        dest = destination[0]
        sorc = source[1] + leftDelta
        ran = rangeSource - leftDelta
        overlap = overlap + [dest, sorc, ran]
        
        return overlap
    elif (intStartfromDest <= intStartfromSource and intEndfromDest <= intEndfromSource): #TODO exclude the == inclusion at limits
        leftDelta = intStartfromSource - intStartfromDest

        dest = destination[0] + leftDelta
        sorc = source[1]
        ran = rangeDest - leftDelta
        overlap = overlap + [dest, sorc, ran]
        
        return overlap
    else:
        return overlap


# Partition map entry, given limits at SOURCE value
def partitionMapEntry(map, start, end):
    # useful
    topRange = start - map[1]
    midRange = end - start + 1
    botRange = map[2] - topRange - midRange
    
    # start, end are in source limits
    leftExclusivePartion = []
    inclusivePartition = []
    rightExclusivePartion = []
    
    # partition process (make function if not lazy...)
    if topRange > 0:
        destination = map[0]
        source = map[1]
        range = topRange
        leftExclusivePartion = leftExclusivePartion + [destination, source, range]
    if midRange > 0:
        destination = map[0] + topRange
        source = map[1] + topRange
        range = midRange
        inclusivePartition = inclusivePartition + [destination, source, range]
    if botRange > 0:
        destination = map[0] + topRange + midRange
        source = map[1] + topRange + midRange
        range = botRange
        rightExclusivePartion = rightExclusivePartion + [destination, source, range]

    return leftExclusivePartion, inclusivePartition, rightExclusivePartion

# Main Loop through 
def main():
    # constants
    file = 'input'
    outputPart1  = "Puzzle answer for Part 1: "
    outputPart2  = "Puzzle answer for Part 2: "
    
    # load data
    bigMap = recordData(file)

    # solution routines called
    solPart1 = findMinLocationPart1(bigMap)
    solPart2 = findMinLocationPart2(bigMap)
    print(outputPart1, solPart1)
    print(outputPart2, solPart2)

if __name__ == "__main__":
    main()