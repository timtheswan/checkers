#Example opponent using heuristics rather than lookaheads, not my code

import random
import copy

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

def findJumpBlockOpponent(playerJumps,opponentMoves):
    blockMovesList=[]
    for jump in playerJumps:
        for move in opponentMoves:
            if jump[-2:] in move:
                blockMovesList.append(jump)
    return blockMovesList
        
def protectHomeRow(board, player,playerMoves):
    protectHomeList=[]
    if player=="b":
        for move in playerMoves:
            if move[0:1]=="H":
                protectHomeList.append(move)
    else:
        for move in playerMoves:
            if move[0:1]=="A":
                protectHomeList.append(move)
    return protectHomeList

def getRegularMoves(board,player,playermoves):
    homeRowMovesList=[]
    regularMovesList=[]
    if player=="b":
        for move in playermoves:
            if move[0:1]!="H":
                regularMovesList.append(move)
            else:
                homeRowMovesList.append(move)
    else:
        for move in playermoves:
            if move[0:1]!="A":
                regularMovesList.append(move)
            else:
                homeRowMovesList.append(move)
    return regularMovesList    

def takeLongestJump(board,player,playerJumps):
    bestJump="0"
    for jump in playerJumps:
        if len(jump) > len(bestJump):
            bestJump=jump
    return bestJump

def wontGetJumped(board,player,playerMoves,opponentMoves):
    badMovesList=[]
    for theirMove in opponentMoves:
        for myMove in playerMoves:
            if myMove[-2:]==theirMove[3:5] and myMove not in badMovesList:
                badMovesList.append(myMove)
    for eachMove in badMovesList:
        if eachMove in playerMoves:
            playerMoves.remove(eachMove)
    return playerMoves
        

def blockLongestJump(board,player,opponentJumps):
    blockJump="0"
    for jump in opponentJumps:
        if len(jump) > len(blockJump):
            blockJump=jump
    return blockJump

def moveToSideSpaces(board,player,playerMoves):
    sideMovesList=[]
    for move in playerMoves:
        if move[4]=="0" or move[4]=="7":
            sideMovesList.append(move)
    return sideMovesList

def blockKingMove(player,playerMoves,opponentMoves):
    blockKingMove=[]
    if player=="r":
        for theirMove in opponentMoves:
            if theirMove[3]=="A":
                for myMove in playerMoves:
                    if myMove[3:]==theirMove[3:]:
                        blockKingMove.append(myMove)
    else:
        for theirMove in opponentMoves:
            if theirMove[3]=="H":
                for myMove in playerMoves:
                    if myMove[3:]==theirMove[3:]:
                        blockKingMove.append(myMove)
    #print("blocking king move",blockKingMove)
    return blockKingMove 

def inbetweenMoves(board,player,playerMoves):
    inbetweenMovesList=[]
    validRange=[0,1,2,3,4,5,6,7]
    for moves in playerMoves:
        newBoard=copy.deepcopy(board)
        row=ord(moves[-2])-65
        col=int(moves[-1])
        fromRow=ord(moves[0])-65
        fromCol=int(moves[1])
        newBoard[fromRow][fromCol]="e"
        if player=="r":
            if row-1 in validRange and col-1 in validRange and row+1 in validRange and col+1 in validRange:
                if (newBoard[row-1][col-1]!="e" and newBoard[row+1][col+1]!="e" and newBoard[row+1][col-1]=="e"):
                    inbetweenMovesList.append(moves)
                if (newBoard[row-1][col+1]!="e" and newBoard[row+1][col-1]!="e" and newBoard[row+1][col+1]=="e"):
                    inbetweenMovesList.append(moves)
        if player=="b":
            if row-1 in validRange and col-1 in validRange and row+1 in validRange and col+1 in validRange:
                if (newBoard[row-1][col-1]!="e" and newBoard[row+1][col+1]!="e" and newBoard[row-1][col+1]=="e"):
                    inbetweenMovesList.append(moves)
                if (newBoard[row+1][col-1]!="e" and newBoard[row-1][col+1]!="e" and newBoard[row+1][col+1]=="e"):
                    inbetweenMovesList.append(moves)
        if player=="R" or player=="B":
            if row-1 in validRange and col-1 in validRange and row+1 in validRange and col+1 in validRange:
                if (newBoard[row-1][col-1]!="e" and newBoard[row+1][col+1]!="e" and newBoard[row+1][col-1]=="e"):
                    inbetweenMovesList.append(moves)
                if (newBoard[row-1][col+1]!="e" and newBoard[row+1][col-1]!="e" and newBoard[row+1][col+1]=="e"):
                    inbetweenMovesList.append(moves)
                if (newBoard[row-1][col-1]!="e" and newBoard[row+1][col+1]!="e" and newBoard[row-1][col+1]=="e"):
                    inbetweenMovesList.append(moves)
                if (newBoard[row+1][col-1]!="e" and newBoard[row-1][col+1]!="e" and newBoard[row+1][col+1]=="e"):
                    inbetweenMovesList.append(moves) 
    # print("between",inbetweenMovesList)
    return inbetweenMovesList

def inbetweenJumps(board,player,playerJumps):
    inbetweenJumpsList=[]
    validRange=[0,1,2,3,4,5,6,7]
    #print("player jumps",playerJumps)
    for moves in playerJumps:
        newBoard=copy.deepcopy(board)
        row=ord(moves[-2])-65
        col=int(moves[-1])
        fromRow=ord(moves[0])-65
        fromCol=int(moves[1])
        newBoard[fromRow][fromCol]="e"
        if player=="r":
            if row-1 in validRange and col-1 in validRange and row+1 in validRange and col+1 in validRange:
                if (newBoard[row-1][col-1]!="e" and newBoard[row+1][col+1]!="e" and newBoard[row+1][col-1]=="e"):
                    inbetweenJumpsList.append(moves)
                if (newBoard[row-1][col+1]!="e" and newBoard[row+1][col-1]!="e" and newBoard[row+1][col+1]=="e"):
                    inbetweenJumpsList.append(moves)
        if player=="b":
            if row-1 in validRange and col-1 in validRange and row+1 in validRange and col+1 in validRange:
                if (newBoard[row-1][col-1]!="e" and newBoard[row+1][col+1]!="e" and newBoard[row-1][col+1]=="e"):
                    inbetweenJumpsList.append(moves)
                if (newBoard[row+1][col-1]!="e" and newBoard[row-1][col+1]!="e" and newBoard[row+1][col+1]=="e"):
                    inbetweenJumpsList.append(moves)
        if player=="R" or player=="B":
            if row-1 in validRange and col-1 in validRange and row+1 in validRange and col+1 in validRange:
                if (newBoard[row-1][col-1]!="e" and newBoard[row+1][col+1]!="e" and newBoard[row+1][col-1]=="e"):
                    inbetweenJumpsList.append(moves)
                if (newBoard[row-1][col+1]!="e" and newBoard[row+1][col-1]!="e" and newBoard[row+1][col+1]=="e"):
                    inbetweenJumpsList.append(moves)
                if (newBoard[row-1][col-1]!="e" and newBoard[row+1][col+1]!="e" and newBoard[row-1][col+1]=="e"):
                    inbetweenJumpsList.append(moves)
                if (newBoard[row+1][col-1]!="e" and newBoard[row-1][col+1]!="e" and newBoard[row+1][col+1]=="e"):
                    inbetweenJumpsList.append(moves)
    # print("between jumps:",inbetweenJumpsList)
    return inbetweenJumpsList

def jumpKingsFirst(board,player,playerJumps):
    # print("playerJumps",playerJumps)
    kingJumpsList=[]
    validRange=[0,1,2,3,4,5,6,7]
    for moves in playerJumps:
        row=ord(moves[-2])-65
        col=int(moves[-1])
        if player=="r" or player=="R":
            if row-1 in validRange and col-1 in validRange and row+1 in validRange and col+1 in validRange:
                if board[row-1][col+1] == "B":
                    kingJumpsList.append(moves)
                if board[row-1][col-1] == "B":
                    kingJumpsList.append(moves)
        if player=="b" or player=="B":
            if row-1 in validRange and col-1 in validRange and row+1 in validRange and col+1 in validRange:
                if board[row+1][col+1] == "R":
                    kingJumpsList.append(moves)
                if board[row+1][col-1] == "R":
                    kingJumpsList.append(moves)
    # print("kingJumpsList",kingJumpsList)
    return kingJumpsList

                                                                   
def getValidMove(board,player):
    #print(protectHomeList)
    if player=="b":
        playerName="black"
        opponent="r"
    else:
        playerName="red"
        opponent="b"

    
    movesList=listValidMoves(board,player)
    jumpsList=listSingleJumps(board,player)
    jumpsList=listMultipleJumps(board,player,jumpsList)
    opponentMovesList=listValidMoves(board,opponent)
    opponentJumpsList=listSingleJumps(board,opponent)
    notHomeRowMove=getRegularMoves(board,player,movesList)
    wontGetJumpedMoves=wontGetJumped(board,player,notHomeRowMove,opponentMovesList)
    wontGetJumpedJumps=wontGetJumped(board,player,jumpsList[:],opponentMovesList)
    moveToSideSquares=moveToSideSpaces(board,player,notHomeRowMove)

    
    #Get player move options
    crowningJumps=findCrownRowMovesOrJumps(board,player,jumpsList)
    crowningMoves=findCrownRowMovesOrJumps(board,player,movesList)
    protectHomeRowMoves=protectHomeRow(board,player,movesList)
    longJump=takeLongestJump(board,player,jumpsList[:])
    notHomeRowMove=getRegularMoves(board,player,movesList)
    homeRowMoves=protectHomeRow(board, player,movesList)

    #Get opponent move options
    opponentMovesList=listValidMoves(board,opponent)
    opponentJumpsList=listSingleJumps(board,opponent)
    opponentJumpsList=listMultipleJumps(board,opponent,opponentJumpsList)
    opponentCrowningJumps=findCrownRowMovesOrJumps(board,opponent,opponentJumpsList)
    opponentCrowningMoves=findCrownRowMovesOrJumps(board,opponent,opponentMovesList)
    longBlockJump=blockLongestJump(board,opponent,opponentJumpsList)
    moveInbetween=inbetweenMoves(board,player,movesList)
    jumpsInbetween=inbetweenJumps(board,player,jumpsList)
    blockKing=blockKingMove(player,movesList,opponentMovesList)
    jumpKing=jumpKingsFirst(board,player,jumpsList)

    

    if crowningJumps !=[]: #Heuristic 3 (crowning jumps)
        return crowningJumps[random.randrange(0,len(crowningJumps))]
    if jumpsList != []: #Heuristic 1 (jumps)
        if opponentCrowningJumps !=[]: #Heuristic 5 (block opponent crowning jumps)
            blocking = findJumpBlockOpponent(jumpsList,opponentCrowningJumps)
            if blocking != []:
                for blockMove in blocking: #Heuristic 12 (always block the longest jump)
                    if blockMove[-2:]==longBlockJump[3:5]:
                        return blockMove
                    else:
                        return blocking[random.randrange(len(blocking))]
        if opponentCrowningMoves != []: #Heuristic 6 (block opponent crowning moves with a jump)
            blocking = findJumpBlockOpponent(jumpsList,opponentCrowningMoves)
            if blocking != []:
                for blockMove in blocking:
                    if blockMove[-2:]==longBlockJump[3:5]:
                        return blockMove
                    else:
                        return blocking[random.randrange(len(blocking))]
        if opponentJumpsList != []: #Heuristic 7 (block opponent jump)
            blocking = findJumpBlockOpponent(jumpsList,opponentJumpsList)
            if blocking != []:
                for blockMove in blocking:
                    if blockMove[-2:]==longBlockJump[3:5]:
                        return blockMove
        if jumpKing!=[]: #Heuristic 17 (jump a king checker instead of a regular checker)
            return takeLongestJump(board,player,jumpKing)
        if wontGetJumpedJumps!=[]: #Heuristic 11 (don't take jumps that will get you jumped back)
            return takeLongestJump(board,player,wontGetJumpedJumps) #Heuristic 8 (always take the longest jump)
        if jumpsInbetween!=[]: #Heuristic 15 (jump to a spot inbetween two checkers)
            return takeLongestJump(board,player,jumpsInbetween)
        else:
            return longJump
    if crowningMoves != []: #Heuristic 4 (take crowning move)
        return crowningMoves[random.randrange(0,len(crowningMoves))]
    if notHomeRowMove!= []: #Heuristic 2 (take a move)
        if blockKing!=[]:
            return blockKing[random.randrange(0,len(blockKing))]
        if moveInbetween != []: #Heuristic 14 (move inbetween two checkers)
            return moveInbetween[random.randrange(0,len(moveInbetween))]
        if wontGetJumpedMoves!=[]: #Heuristic 10 (take moves that won't get you jumped)
            return wontGetJumpedMoves[random.randrange(0,len(wontGetJumpedMoves))]
        if moveToSideSquares!=[]:#Heuristic 13 (Move to side squares when possible)
            return moveToSideSquares[random.randrange(0,len(moveToSideSquares))]
        return notHomeRowMove[random.randrange(0,len(notHomeRowMove))]
    else: # Heuristic 9 (don't move from the home row unless it's your only option for a move)
        return homeRowMoves[random.randrange(0,len(homeRowMoves))]
        
