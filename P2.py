#My player, using Minimax, pruning, internal heuristics, and several additional optimizations.

import copy
import time
import math
debug=False
globalLevel = 4
globalBench = 4
timeRestriction=True
startTime=time.time()
moveHistory=[]
moveLenHistory=[]
moveTimeHistory=[]
pruned=0
notPruned=0
compLevel=0
stats={}
diagnostics=True

def listValidMoves(board,player):
    possibleMoves=[]
    validRange=[0,1,2,3,4,5,6,7] #list(range(8))
    if player=="b":
        playerTokens=["b","B"]
        moveRowInc=-1
    else:
        playerTokens=["r","R"]
        moveRowInc=1
    kingTokens=["B","R"]
    for row in range(8): #For every row
        for col in range(8):  #For every square in a row
            if board[row][col] in playerTokens: #If the board contains either a regular or king checker of the given player
                if board[row][col] not in kingTokens: #if checker is NOT a king
                    for colInc in [-1,1]: #for each diagonal square in the correct row direction
                        if row+moveRowInc in validRange and col+colInc in validRange and board[row+moveRowInc][col+colInc] =='e':
                            possibleMoves.append(chr(row+65)+str(col)+":"+chr(row+65+moveRowInc)+str(col+colInc))
                else:  #checker is a king
                    for rowInc in [-1,1]: #for each row direction (forward and backward)
                        for colInc in [-1,1]: #for each diagonal square in each row direction
                            if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc] =='e':
                                possibleMoves.append(chr(row+65)+str(col)+":"+chr(row+65+rowInc)+str(col+colInc))
    return possibleMoves

def listSingleJumps(board,player):
    possibleSingleJumps=[]
    validRange=[0,1,2,3,4,5,6,7] #list(range(8))
    if player=="b":
        playerTokens=["b","B"]
        rowInc=-1
        enemyTokens=["r","R"]
    else:
        playerTokens=["r","R"]
        rowInc=1
        enemyTokens=["b","B"]
    kingTokens=["B","R"]
    for row in range(8):
        for col in range(8):
            if board[row][col] in playerTokens:
                if board[row][col] not in kingTokens:  #if checker is NOT a king
                    for colInc in [-1,1]:
                        if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc] in enemyTokens:
                            colJumpInc=2 * colInc
                            rowJumpInc=2 * rowInc
                            if row+rowJumpInc in validRange and col + colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e":
                                possibleSingleJumps.append(chr(row+65)+str(col)+":"+chr(row+65+rowJumpInc)+str(col+colJumpInc))
                else: #checker is a king
                    for rowIncs in [-1,1]: #for each row direction (forward and backward)
                        for colInc in [-1,1]:
                            if row+rowIncs in validRange and col+colInc in validRange and board[row+rowIncs][col+colInc] in enemyTokens:
                                colJumpInc=2 * colInc
                                rowJumpInc=2 * rowIncs
                                if row+rowJumpInc in validRange and col + colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e":
                                    possibleSingleJumps.append(chr(row+65)+str(col)+":"+chr(row+65+rowJumpInc)+str(col+colJumpInc))
    return possibleSingleJumps

def listMultipleJumps(board,player,jumpsList):
    newJumps=expandJumps(board,player,jumpsList)
    while newJumps != jumpsList:
        jumpsList=newJumps[:]
        newJumps=expandJumps(board,player,jumpsList)
    return newJumps

def expandJumps(board,player,oldJumps):
    INCs=[1,-1]
    VALID_RANGE=[0,1,2,3,4,5,6,7]
    if player=="b":
        playerTokens=["b","B"]
        rowInc=-1
        opponentTokens=["r","R"]
    else:
        playerTokens=["r","R"]
        rowInc=1
        opponentTokens=["b","B"]
    newJumps=[]
    for oldJump in oldJumps:
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        startRow=ord(oldJump[0])-65
        startCol=int(oldJump[1])
        if board[startRow][startCol] not in ["R","B"]: #not a king
            for colInc in INCs:
                jumprow=row+rowInc
                jumpcol=col+colInc
                torow=row+2*rowInc
                tocol=col+2*colInc
                if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                and board[jumprow][jumpcol] in opponentTokens and board[torow][tocol]=='e':
                    newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                    if oldJump in newJumps:
                        newJumps.remove(oldJump)
        else: #is a king
            for colInc in INCs:
                for newRowInc in INCs:
                    jumprow=row+newRowInc
                    jumpcol=col+colInc
                    torow=row+2*newRowInc
                    tocol=col+2*colInc
                    if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                    and board[jumprow][jumpcol] in opponentTokens and (board[torow][tocol]=='e' or oldJump[0:2]==chr(torow+65)+str(tocol)) \
                    and ((oldJump[-2:]+":"+chr(torow+65)+str(tocol)) not in oldJump) and ((chr(torow+65)+str(tocol)+':'+oldJump[-2:] not in oldJump)) and (chr(torow+65)+str(tocol)!=oldJump[-5:-3]):
                        newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                        if oldJump in newJumps:
                            newJumps.remove(oldJump)
    return newJumps

def findCrownRowMovesOrJumps(board,player,movesList):
    kingingList=[]
    for move in movesList:
        FROM=move[0:2]
        FROMRow=ord(FROM[0])-65
        FROMCol=int(FROM[1])
        TO=move[-2:]
        TORow=TO[0]
        if player=="r":
            kingRow="H"
        else:
            kingRow="A"
        if board[FROMRow][FROMCol]==player and TORow==kingRow:
            kingingList.append(move)
            movesList=movesList[:movesList.index(move)]+movesList[movesList.index(move)+1:]
    return kingingList

def listCrowningMoves(board,player,movesList):
    crowningMoves=[]
    for i in range(len(movesList)):
        if movesList[i][-2]=='A' and player=='b' and not board[ord(movesList[i][0])-65][int(movesList[i][1])]=='B':
            crowningMoves.append(movesList.pop(i))
        elif movesList[i][-2]=='H' and player=='r'and not board[ord(movesList[i][0])-65][int(movesList[i][1])]=='R':
            crowningMoves.append(movesList.pop(i))
        return crowningMoves,movesList

def listCrowningJumps(board,player,jumpsList):

    crowningJumps = []
    jumpsDupe=jumpsList[:]
    removes=[]
    if len(jumpsList)==0:
        return crowningJumps,jumpsList
    for i in range(len(jumpsList)):
        if 'A' in jumpsDupe[i] and player == 'b' and not board[int(jumpsDupe[i][1])][ord(jumpsDupe[i][0])-65]=='B':
            crowningJumps.append(jumpsDupe[i])
            removes.append(i)
        elif 'H' in jumpsDupe[i] and player == 'r' and not board[int(jumpsDupe[i][1])][ord(jumpsDupe[i][0])-65]=='R':
            crowningJumps.append(jumpsDupe[i])
            removes.append(i)
    for i in range(len(removes)-1,-1,-1):
        jumpsList.pop(removes[i])
    return crowningJumps,jumpsList

def generateMoves(board,player):

    moves = listValidMoves((board), player)
    jumps = listSingleJumps((board), player)
    jumps = listMultipleJumps((board), player, jumps)

    crowningMoves = []
    crowningJumps = []

    if not moves == []:
        crowningMoves, moves = listCrowningMoves((board), player, moves)
    if not jumps == []:
        crowningJumps, jumps = listCrowningJumps((board), player, jumps)

    if len(jumps)+len(crowningJumps) > 0:  # If jumps are an option, only include them in possible moves
        allMoves = crowningJumps + jumps

    else:
        allMoves = crowningJumps + crowningMoves + jumps + moves

    return allMoves

def clock():
    global startTime
    return time.time()-startTime

def parseMove(move):
    FROM=move[0:2]
    FROMRow=ord(FROM[0])-65
    FROMCol=int(FROM[1])
    TO=move[3:5]
    TORow=ord(TO[0])-65
    TOCol=int(TO[1])
    return FROMRow,FROMCol,TORow,TOCol

def printBoard(board):
    for row in range(8):
        for col in range(8):
            print("",board[row][col],end="")
        print()
    print()

def evalBoard(board, level):  # Black is Negative, Red is Positive

    Bscore = 0.0
    Rscore = 0.0
    rCheckers=[]
    bCheckers=[]
    bKingRatio=0
    rKingRatio=0
    for i in range(len(board)):  # Heuristic 2, evaluate outcomes by the number of normal pieces and kings and choose accordingly
        for j in range(len(board[i])):
            token=board[i][j]
            if token == 'r':
                rCheckers.append([i,j,'r',0])
                Rscore += 1 * (1 + ((i) / 8))  # Closer to kinging is more valuble
                if i == 0:
                    Rscore += .3  # Keep home row
                rKingRatio-=1
            elif token == 'R':  # Kings are worth 2
                Rscore += 2
                rCheckers.append([i, j, 'R',0])
                rKingRatio+=1
            elif token == 'b':
                Bscore -= 1 * (1 + ((8 - (i+1)) / 8))  # Heuristic 4 Closer to kinging is more valuble
                if i == 7:
                    Bscore -= .3  # Heuristic 3 Keep home row
                bCheckers.append([i, j, 'b',0])
                bKingRatio-=1
            elif token == 'B':  # Kings are worth 2
                Bscore -= 2
                bCheckers.append([i, j, 'B',0])
                bKingRatio+=1
            if (j in range(2,6)):  # Prioritize center Heuristic 8
                if token == 'R' or token == 'r':
                    Rscore += .1
                elif token == 'B' or token == 'b':
                    Bscore -= .1

    # if bKingRatio>=0 or rKingRatio>=0: #If more kings than normal (aka if end of game and approaching stalemate) #Work in progress
    #     for i in range (len(bCheckers)):
    #         sum=0
    #         count=0
    #         for j in range(len(bCheckers)-i-1):
    #             distance=math.sqrt((bCheckers[i][0]-bCheckers[j][0])**2 + (bCheckers[i][1]-bCheckers[j][1])**2)
    #             sum+=distance
    #             count+=1
    #         bCheckers[i][2]=sum/count #Average distance from teamates
    #     for i in range(len(rCheckers)):
    #         sum = 0
    #         count = 0
    #         for j in range(len(rCheckers) - i - 1):
    #             distance = math.sqrt((rCheckers[i][0] - rCheckers[j][0]) ** 2 + (rCheckers[i][1] - rCheckers[j][1]) ** 2)
    #             sum += distance
    #             count += 1
    #         rCheckers[i][2] = sum / count  # Average distance from teamates

    if Bscore > -1:  # Heuristic 5, go for wins, prioritize wins that are in fewer moves
        return 1999 / (globalLevel - level)
    if Rscore < 1:
        return -1999 / (globalLevel - level)

    if abs(Bscore) > Rscore:  # Heuristic 15, take trades if winning to improve ratio, don't take trades if losing, accounts for cases even if piece is already a King
        trade = -Rscore*.2
        Bscore -= trade
    elif Rscore > abs(Bscore):
        trade = -Bscore*.2
        Rscore += trade
    score = Bscore + Rscore
    return score

def applyMove(board, move,player):
    FROMRow, FROMCol, TORow, TOCol = parseMove(move)

    if abs(FROMRow - TORow) == 1:  # move, not a jump
        playerToken = board[FROMRow][FROMCol]  # save the player form current location (regular checker or king)
        board[FROMRow][FROMCol]= 'e'
        board[TORow][TOCol]=playerToken
    else:  # jump, not a move
        reps = move.count(":")
        for i in range(reps):
            FROMRow, FROMCol, TORow, TOCol = parseMove(move)
            playerToken = board[FROMRow][FROMCol]  # save the player form current location (regular checker or king)
            board[FROMRow][FROMCol]= 'e'  # remove the checker to be moved
            board[TORow][TOCol]=playerToken
            board[(FROMRow + TORow) // 2][(FROMCol + TOCol) // 2]= 'e' # remove the jumped checker
            move = move[3:]

    if playerToken == "r" and TORow == 7:  # if a kinging move for red
        board[TORow][TOCol] = playerToken.upper()
    elif playerToken == "b" and TORow == 0:  # if a kinging move for black
        board[TORow][TOCol] = playerToken.upper()

    return board

def miniMax(board,player,level,moveHistory,alpha,beta): #Positive is Red advandage, Negative is Black
    if player == 'r':
        sign=1
        enemy='b'
    else:
        sign=-1
        enemy='r'

    if timeRestriction and clock() > .98:  # Prevent timeout
        return (-2000*sign,'Timeout')

    allMoves=generateMoves(board,player)
    if level==globalLevel and len(allMoves)==1:
        return('oy',allMoves[0])
    if len(allMoves)==0: #Is end of game
        return(-1010*sign,'end of game')

    if level == 0: #Evaluate Board
        return evalBoard(copy.deepcopy(copy.deepcopy(board)),level),allMoves[0]

    bestVal=-2000*sign
    bestMove=''

    for i in allMoves:
        if timeRestriction and clock()>.98:
            break

        temp=copy.deepcopy(moveHistory)
        temp.append(i)

        val,trash=miniMax(applyMove(copy.deepcopy(board),i,(player)),enemy,level-1,temp,alpha,beta)#Recursive Call

        # val+=(len(i)-5)//3*sign #Heuristic 1, increase value of jumps by their legnth

        if len(moveHistory)>3 and i==temp[-3] and temp[-2][:2]==i[3:]: #Heuristic 7, do not make repetitive moves
            val-=(sign*.5)
        if len(moveHistory)>5 and i==temp[-5] and temp[-4][:2]==i[3:]: #Heuristic 7.5, do not make doubly repetitive moves
            val-=(sign)

        if player == 'r':#Choose better move
            if val>bestVal:
                bestVal = val
                bestMove = i
                alpha=max(alpha,val)
                if beta<=alpha:
                    # pruned+=1
                    break
        else:
            if val<bestVal:
                bestVal=val
                bestMove=i
                beta=min(beta,val)
                if beta <= alpha:
                    # pruned+=1
                    break
        # notPruned+=1
    return bestVal,bestMove


def isGameStart(board): #Identify if this is the first time running for the game in order to return a hardcoded first move and use the second to run computer diagnostics
    startBoard=generateStartBoard()
    if board==startBoard and debug:
        print('May the best player win!')
        return True
    if board[:3]==startBoard[:3] and debug:
        print ('May the best player win!')
        return True
    if board[5:]==startBoard[5:] and debug:
        print ('May the best player win!')
        return True
    return False

def generateStartBoard():
    board=[["r", "e", "r", "e", "r", "e", "r", "e"],
           ["e", "r", "e", "r", "e", "r", "e", "r"],
           ["r", "e", "r", "e", "r", "e", "r", "e"],
           ["e", "e", "e", "e", "e", "e", "e", "e"],
           ["e", "e", "e", "e", "e", "e", "e", "e"],
           ["e", "b", "e", "b", "e", "b", "e", "b"],
           ["b", "e", "b", "e", "b", "e", "b", "e"],
           ["e", "b", "e", "b", "e", "b", "e", "b"]]

    return board

def compDiagnostics ():#Heuristic 11: Figure out the speed of the computer at the start of the game and create a level modifier that will influence the level the player goes to
    global globalLevel
    global compLevel
    board8 =        [["r", "e", "r", "e", "r", "e", "r", "e"],
                    ["e", "r", "e", "r", "e", "r", "e", "r"],
                    ["e", "e", "r", "e", "r", "e", "r", "e"],
                    ["e", "r", "e", "e", "e", "e", "e", "e"],
                    ["e", "e", "e", "e", "e", "e", "b", "e"],
                    ["e", "b", "e", "b", "e", "b", "e", "e"],
                    ["b", "e", "b", "e", "b", "e", "b", "e"],
                    ["e", "b", "e", "b", "e", "b", "e", "b"]]#Scenario with a moveslist of legnth 8
    board10 = [["r", "e", "r", "e", "r", "e", "e", "e"],
                       ["e", "r", "e", "r", "e", "r", "e", "e"],
                       ["e", "e", "r", "e", "r", "e", "e", "e"],
                       ["e", "r", "e", "e", "e", "e", "e", "e"],
                       ["e", "e", "e", "e", "e", "e", "b", "e"],
                       ["e", "R", "e", "b", "e", "b", "e", "e"],
                       ["e", "e", "b", "e", "b", "e", "b", "e"],
                       ["e", "b", "e", "b", "e", "b", "e", "b"]]#Scenario with a moveslist of legnth 10 (not used)
    storeLevel=globalLevel

    globalLevel = 5
    start = time.time()
    #time.sleep(.4)#Use this to simulate a slow computer
    trash,move = miniMax(board8, 'r', 5, [], -2000, 2000)
    timeTook = time.time()-start
    print('The test took %1.3f seconds'%(timeTook))


    if timeTook<.18:
        compLevel=1
    elif timeTook<.4:
        compLevel=0
    else:
        compLevel=-1
    print("The computer level is:",compLevel)
    globalLevel=storeLevel
    return timeTook
def getValidMove(board, player):
    global startTime
    global globalLevel
    global globalBench
    global moveLenHistory
    global moveHistory
    moves=generateMoves(board,player)
    startTime = time.time()
    #if isGameStart(board):
    if moveHistory==[] and diagnostics:
        print('Minimax Player is color: ',player)
        timee=compDiagnostics()
        if debug: print('Returning hardcoded move')
        if player == 'r':
            move='C4:D3'
            if move in moves:
                moveHistory.append(move)
                moveLenHistory.append(1)
                moveTimeHistory.append(timee)
                return ('C4:D3')
            else:
                moveHistory.append(moves[0])
                moveLenHistory.append(1)
                moveTimeHistory.append(timee)
                return (moves[0])
        else:
            move = ('F5:E4')
            if move in moves:
                moveHistory.append(move)
                moveLenHistory.append(1)
                moveTimeHistory.append(timee)
                return move
            else:
                moveHistory.append(moves[0])
                moveLenHistory.append(1)
                moveTimeHistory.append(timee)
                return moves[0]

    num = len(generateMoves(board, player))  # Heuristic 12, look deeper when easier, as estimated by the initial amount of  moves, numbers fine tuned to minimize the timeout rate while maximizing use of time.
    # print(num)

    if moveLenHistory != [] and abs(moveLenHistory[-1]-num)<=3: # Heuristic 14, determine lookahead level by history, If board complexity similar to last move, and last move was short, increase level by one, if last move timed out, decrease level by one, else reuse last level
        if moveTimeHistory[-1]<.25: #If last move was too fast
            globalLevel+=1
            if debug: print('Increasing Level')
        elif moveTimeHistory[-1]>.80: #If last move was too slow
            globalLevel-=1
            if debug: print('Decreasing Level')
        if globalLevel>=7:
            globalLevel=6
            if debug: print('Undoing level increase')
    elif  len(moveLenHistory)>1 and abs(moveLenHistory[-2]-num)<=3 and moveLenHistory[-1]==1: #Accounting for jumps
        pass
    elif num <= 5:
        globalLevel = globalBench + compLevel + 2
    elif num <= 7:
        globalLevel = globalBench + compLevel + 1
    elif num <= 13:
        globalLevel = globalBench
    elif num <= 16:
        globalLevel = globalBench + compLevel - 1  # Heuristic 13, look less deep when harder, to lower occurences of timeout, also impliment the computer speed modifier
    else:
        globalLevel = globalBench + compLevel - 2
    if debug: print('With %d possible moves, I am looking %d moves ahead'%(num,globalLevel))
    # print(startTime%60)
    if player == 'b':
        enemy = 'r'
    else:
        enemy = 'b'
    trash, move = miniMax(board, player, globalLevel, copy.deepcopy(moveHistory), -2000, 2000)

    if move == '':
        allMoves = generateMoves(board, player)
        if debug: print('Invalid Move Backup')
        return allMoves[0]
    if clock()>= .98:
        if debug: print('Lookahead timeout')
    if clock() > .9999:
        print('I know I timed out at %2.3f seconds' % (clock()))

    moveHistory.append(move)
    moveLenHistory.append(num)
    # print('I took this long: %1.4f, and looked %d levels deep'%(clock(),globalLevel))
    if stats.get(globalLevel, -1) == -1:
        stats[globalLevel] = [0, 0, 0]
    stats[globalLevel][0] += clock()
    stats[globalLevel][1] += 1
    if clock() >= .98:
        stats[globalLevel][2] += 1
    if len(moveHistory) ==99 and debug:
        for i in stats:
            # print(type(i),type(stats[i][0]/stats[i][1]),type(stats[i][2]/stats[i][1]))
            print('For level %d, the average time was %1.4f with %.3f percent of overtime moves' % (
            i, stats[i][0] / stats[i][1], stats[i][2] * 100 / stats[i][1]))
        # print(stats)

    moveTimeHistory.append(clock())
    if debug: print('Returning move of:',move)
    return move

board10 = [["r", "e", "e", "e", "e", "e", "e", "e"],
                       ["e", "e", "e", "e", "e", "e", "e", "e"],
                       ["e", "e", "e", "e", "e", "e", "e", "e"],
                       ["e", "e", "e", "e", "e", "e", "e", "e"],
                       ["e", "e", "e", "e", "e", "e", "e", "e"],
                       ["e", "e", "e", "e", "e", "e", "e", "e"],
                       ["e", "e", "e", "e", "e", "e", "e", "e"],
                       ["e", "e", "e", "e", "e", "e", "e", "b"]]
