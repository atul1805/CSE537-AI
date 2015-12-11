def readGameState(filePath):
    fileHandle = open(filePath, 'r')
    
    firstLine = fileHandle.readline().strip().split(',')
    N = int(firstLine[0])
    M = int(firstLine[1])
    K = int(firstLine[2][:-1]) # Drop the semicolon
    
    sudokuBoard = [[0 for x in range(N)] for x in range(N)]
    for i in range(N):
        line = fileHandle.readline().strip().split(',')
        for j in range(N):
            if j == (N-1):
                line[j] = line[j][:-1] # Drop the semicolon
            if line[j] == '-':
                sudokuBoard[i][j] = 0
            elif line[j] >= 1 or line[j] <= N:
                sudokuBoard[i][j] = int(line[j])
            else:
                print "Invalid Number in game state, check txt file"
                exit(0)
    return (sudokuBoard,N,M,K)
