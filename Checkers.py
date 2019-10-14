import turtle
import random
import time
import P1
import P2
import copy


whoStarts=[0,0]
SLOW_DOWN=False
step=False
graphics=True
timeTest=False
enforceTime=True
p1time=[0,0,0]
p2time=[0,0,0]
moveCounter=0
maxMoves=150
masterTime=time.time()
def drawSquare(t,color):
    if graphics:
        t.color("black")
        t.fillcolor(color)
        t.begin_fill()
        for num in range(4):
            t.forward(1)
            t.right(90)
        t.end_fill()

def drawRow(t,color1,color2):
    if graphics:

        for i in range(4):
            drawSquare(t,color1)
            t.forward(1)
            drawSquare(t,color2)
            t.forward(1)

def drawChecker(t,row,col,color,kingFlag):
    if graphics:
        y=row-1
        x=col+.5
        t.color("dimgray",color)
        t.up()
        t.goto(x,y)
        t.down()
        t.begin_fill()
        t.circle(.5)
        t.end_fill()
        #draw the concentric circles in the checker
        for i in range(1,5):
            t.up()
            t.goto(x,y+(i*.1))
            t.down()
            if i==4 and kingFlag:
                t.begin_fill()
                t.color("yellow")
            t.circle(.5-(i*.1))
            if i==4 and kingFlag:
                t.end_fill()
                t.color("dimgray")

def drawBoard(bob):
    if graphics:
        c1="gray"
        c2="red"
        for x in range(8):
            drawRow(bob,c1,c2)
            bob.up()
            bob.goto(0,x+1)
            bob.down()
            #switch c1 and c2 colors
            temp=c1
            c1=c2
            c2=temp
        drawLabels(bob)

def drawLabels(t):
    if graphics:
        offset=0
        t.color("white")
        for line in "ABCDEFGH":
            for cell in range(0,8,2):
                t.up()
                t.goto(offset+cell+.82,ord(line)-65+.02)
                t.down()
                t.write(line+str(cell+offset))
            if offset==0:
                offset=1
            else:
                offset=0
        t.color("black")

def drawLabel(t,row,col):
    if graphics:
        t.color("white")
        t.up()
        t.goto(col+.82,row+.02)
        t.down()
        t.write(chr(row+65)+str(col))
        t.color("black")

def printBoard(board):
    for row in range(8):
        for col in range(8):
            print("",board[row][col],end="")
        print()
    print()

def populateBoardsWithCheckers(t,board):
    offset=0
    t.color("red")
    for row in range(0,3):
        for col  in range(0,8,2):
            if graphics:
                drawChecker(t,row,col+offset,"red",False)
            board[row][col+offset]="r"
        if offset==0:
            offset=1
        else:
            offset=0
    offset=1
    t.color("black")
    for row in range(5,8):
        for col in range(0,8,2):
            if graphics:
                drawChecker(t,row,col+offset,"black",False)
            board[row][col+offset]="b"
        if offset==1:
            offset=0
        else:
            offset=1

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
               
def swapPlayer(player):
    if player=="b":
        player="r"
        playerColor="red"
    else:
        player="b"
        playerColor="black"
    return player,playerColor

def setupGame(inFileName):
    #Set up graphics for game

    wn=turtle.Screen()
    wn.setworldcoordinates(-2,9,10,-2)
    bob=turtle.Turtle()
    bob.hideturtle()
    wn.tracer(False)
    drawBoard(bob)
    #Set up logical and graphical checkers
    row=["e","e","e","e","e","e","e","e"]
    board=[]
    for i in range(8):
        board.append(row[:])
    if inFileName == "":
        populateBoardsWithCheckers(bob,board)
        if random.randint(0, 1) == 1:
            player = "b"
            print('Player B is starting')
            whoStarts[0]+=1
        else:
            player = "r"
            print('Player R is starting')
            whoStarts[1]+=1
    else:
        inFile=open(inFileName,'r')
        for rowIndex in range(8):
            line=inFile.readline()[:-1]
            for colIndex in range(8):
                if line[colIndex] in ["r","b","R","B"]:
                    board[rowIndex][colIndex]=line[colIndex]
                    if line[colIndex] in ["r","R"]:
                        drawChecker(bob,rowIndex,colIndex,"red",line[colIndex]=="R")
                    else: #black checker
                        drawChecker(bob,rowIndex,colIndex,"black",line[colIndex]=="B")
        player=inFile.readline()[0]
        inFile.close()
    # printBoard(board)
    wn.tracer(True)
    return wn,bob,board,player
    
def parseMove(move):
    FROM=move[0:2]
    FROMRow=ord(FROM[0])-65
    FROMCol=int(FROM[1])
    TO=move[3:5]
    TORow=ord(TO[0])-65
    TOCol=int(TO[1])
    return FROMRow,FROMCol,TORow,TOCol

def removeCheckerGraphicalAndLogical(bob,FROMCol,FROMRow,board):
    bob.up()
    bob.goto(FROMCol,FROMRow)
    bob.down()
    drawSquare(bob,"gray") #empty the graphical square
    drawLabel(bob,FROMRow,FROMCol) #relabel the emptied square
    playerBoardToken=board[FROMRow][FROMCol] #copy the player token from the logical board, could be "b" or "B" or "r" or "R"
    board[FROMRow][FROMCol]='e' #set the logical board location to empty
    return playerBoardToken

def placeCheckerGraphicalAndLogical(bob,TOCol,TORow,board,playerToken):
    #Logical board update first
    if playerToken == "r" and TORow==7:  #if a kinging move for red
        board[TORow][TOCol]=playerToken.upper()
    elif playerToken == "b" and TORow==0: #if a kinging move for black
        board[TORow][TOCol]=playerToken.upper()
    else: #all non-kinging moves place checker in logical board
        board[TORow][TOCol]=playerToken
    #Now graphical board update
    if graphics:
        if board[TORow][TOCol] =="b":
            drawChecker(bob,TORow,TOCol,"black",False)
        elif board[TORow][TOCol] =="B":
            drawChecker(bob,TORow,TOCol,"black",True) #True is King
        elif board[TORow][TOCol] =="r":
            drawChecker(bob,TORow,TOCol,"red",False)
        elif board[TORow][TOCol] =="R": #could have used else, but elif for reading clarity
            drawChecker(bob,TORow,TOCol,"red",True) #True is King

def win(board):
    rmove=listValidMoves(board,"r")
    rjump=listSingleJumps(board,"r")
    rjump=listMultipleJumps(board,"r",rjump)
    bmove=listValidMoves(board,"b")
    bjump=listSingleJumps(board,"b")
    bjump=listMultipleJumps(board,"b",bjump)
    if len(rmove)==0 and len(rjump)==0:
        return [True,"black"]
    if len(bmove)==0 and len(bjump)==0:
        return [True,"red"]
    return [False,""]

def saveGame(fileName,board,player):
    outFile=open(fileName,'w')
    outLine=""
    for row in board:
        for ch in row:
            outLine+=ch
        outFile.write(outLine+"\n")
        outLine=""
    outFile.write(player)
    outFile.close()
    print("Game file saved to",fileName)         

def checkersMain(inFileName,player1,player2):
    wn,bob,board,player=setupGame(inFileName)
    print('           ',player1,'is Red ',player2,'is Black')
    if player=="b":
        playerColor="black"
    else:
        playerColor="red"
    gameOver=False
    if step:
        input('Press enter to procede')
    startingTime = time.time()

    move = getMove(board,player,player1,player2)

    if clock(startingTime)>1 and enforceTime:
        print('Timeout!',player,'took ',clock(startingTime),'seconds!')
        if player=='r':

            return 'b','Player Timeout'
        else:
            return 'r','Player Timeout'
    while move.lower() != "quit" and not gameOver:   #Start alternate play
        wn.tracer(False)
        if step:
            input('Press enter to procede')
        FROMRow,FROMCol,TORow,TOCol=parseMove(move) #parse move into locations
        if abs(FROMRow-TORow)==1: #move, not a jump
            if SLOW_DOWN:
                time.sleep(1)
            playerToken=board[FROMRow][FROMCol] #save the player form current location (regular checker or king)
            removeCheckerGraphicalAndLogical(bob,FROMCol,FROMRow,board) #remove the checker to be moved
            if SLOW_DOWN:
                time.sleep(.5)
            placeCheckerGraphicalAndLogical(bob,TOCol,TORow,board,playerToken) #place the moved checker in its new location
        else: #jump, not a move
            reps=move.count(":")
            for i in range(reps):
                FROMRow,FROMCol,TORow,TOCol=parseMove(move)
                playerToken=board[FROMRow][FROMCol] #save the player form current location (regular checker or king)
                wn.tracer(False)
                if SLOW_DOWN:
                    time.sleep(1)
                removeCheckerGraphicalAndLogical(bob,FROMCol,FROMRow,board) #remove the checker to be moved
                if SLOW_DOWN:
                    time.sleep(.5)
                placeCheckerGraphicalAndLogical(bob,TOCol,TORow,board,playerToken) #place the jumping checker in its new location
                if SLOW_DOWN:
                    wn.tracer(True)
                    time.sleep(1)
                    wn.tracer(False)
                removeCheckerGraphicalAndLogical(bob,(FROMCol+TOCol)//2,(FROMRow+TORow)//2,board) #remove the jumped checker
                if SLOW_DOWN:
                    time.sleep(.5)
                wn.tracer(True)
                move=move[3:]
        wn.tracer(True)
        # printBoard(board)
        player,playerColor=swapPlayer(player)
        gameOver,winningPlayer=win(board)
        if (not gameOver):
            startinggTime = time.time()
            move=getMove(board,player,player1,player2)
        if clock(startinggTime) > 1 and enforceTime:
            print('Player timeout at %4.3f seconds'%(clock(startinggTime)))
            if player == 'r':
                return 'b', 'Player Timeout'
            else:
                return 'r', 'Player Timeout'
        if moveCounter>maxMoves:
            # print('Game ends to too many moves')
            return scoreBoard(board),'Game Timeout'


    # print("Game over, man!!!")
    if move.lower() != "quit":
        # print(scoreBoard(board) +" won the game in a smashing victory!")
        return scoreBoard(board),'Standard'
    else:
        fileName=input("Enter a file name to save the current state of the game, or just hit enter to quit without saving the game => ")
        if fileName != "":
            saveGame(fileName,board,player)
def clock(startTime):
    return time.time()-startTime
def getMove(board,player,player1,player2):#Player 1 is Red
    global moveCounter
    moveCounter += 1
    invalid = True
    validJumps=listSingleJumps(board,player)
    validJumps+=listMultipleJumps(board,player,validJumps)
    validMoves=listValidMoves(board,player)
    startTime=time.time()
    while invalid:
        'Main', 'Dumb', 'Julia', 'Courtney'
        if player == "b":
            if player2=='Main':
                move = Main.getValidMove(copy.deepcopy(board), player)
            elif player2=='Dumb':
                move = Dumb.getValidMove(copy.deepcopy(board), player)
            elif player2=='Julia':
                move = Julia.getValidMove(copy.deepcopy(board), player)
            elif player2=='Courtney':
                move = Courtney.getValidMove(copy.deepcopy(board),player)
            elif player2=='Manual':
                move = Manual.getValidMove(copy.deepcopy(board),player)
            elif player2=='P1':
                move = P1.getValidMove(copy.deepcopy(board),player)
            elif player2=='P2':
                move = P2.getValidMove(copy.deepcopy(board),player)
        else:
            if player1=='Main':
                move = Main.getValidMove(copy.deepcopy(board), player)
            elif player1=='Dumb':
                move = Dumb.getValidMove(copy.deepcopy(board), player)
            elif player1=='Julia':
                move = Julia.getValidMove(copy.deepcopy(board), player)
            elif player1=='Courtney':
                move = Courtney.getValidMove(copy.deepcopy(board),player)
            elif player1=='Manual':
                move = Manual.getValidMove(copy.deepcopy(board),player)
            elif player1=='P1':
                move = P1.getValidMove(copy.deepcopy(board),player)
            elif player1=='P2':
                move = P2.getValidMove(copy.deepcopy(board),player)
        if len(validJumps)>0:
            if move in validJumps:
                invalid=False
            else:
                # print (player, 'must take jump, not ',move)
                if time.time() - startTime > 2 and not 'Manual' in [player1,player2]:
                    print('Timeout due to Missing Jump:',move)
                    # input('Press enter')
                    return ('Timeout')
        else:
            if move in validMoves:
                invalid=False
            else:
                print (player, 'entered invalid move of: ',move)
    # print ('Player %s made the move %s in %3.2f seconds'%(player,move,clock(startTime)))
    if player=='r':
        p1time[0]+=time.time()-startTime
        p1time[1]+=1
        if time.time()-startTime>=.98:
            p1time[2]+=1
    else:
        p2time[0] += time.time() - startTime
        p2time[1] += 1
        if time.time() - startTime >= .98:
            p2time[2] += 1

    return move
def scoreBoard (board):
    Bscore = 0.0
    Rscore = 0.0
    for i in range(len(
            board)):  # Heuristic 2, evaluate outcomes by the number of normal pieces and kings and choose accordingly
        for j in range(len(board[i])):
            if board[i][j] == 'r':
                Rscore += 1  # Closer to kinging is more valuble

            elif board[i][j] == 'R':  # Kings are worth 2
                Rscore += 2

            if board[i][j] == 'b':
                Bscore += 1
            elif board[i][j] == 'B':  # Kings are worth 2
                Bscore += 2
    # print('Score of Black: %d Red: %d'%(Bscore,Rscore))
    if Rscore>Bscore:
        return 'r'
    elif Bscore>Rscore:
        return 'b'
    else:
        return 'tie'
# players=['Main','Dumb','Julia','Courtney']


def competetion (players):
    #checkersMain("heuristic check 8.txt")


    red=0
    black=0
    tie=0


    # players=['Main','Dumb']
    results={}
    for g in players:
        for h in players:
            print('----------Match up of', g, 'vs', h,'----------')
            red=0
            black=0
            tie=0
            for i in range(500):
                global moveCounter
                moveCounter=0
                gameStart = time.time()
                winner,endType=checkersMain('',g,h)
                moveCounter=0
                if winner=='r':
                    red+=1
                elif winner=='b':
                    black+=1
                else:
                    tie+=1

                gameTime=time.time()-gameStart
                mins=gameTime//60
                gameTime-=mins*60
                print('The score is now Red:',red,' Black:',black,'Ties:',tie)
                print('The game took %d minutes and %2.1f seconds, and ended for the reason: %s'%(mins,gameTime,endType))
            results[(g + ' vs ' + h)] = [red,black,tie]
    print('')
    for i in results:
        print('In the matchup',i, 'the results were:',results[i])
    entireTime=time.time()-masterTime
    hours=entireTime//(60*60)
    mins=(entireTime-(hours*60*60))//60
    seconds=int(entireTime-hours*60*60-mins*60)
    print('')
    print('The entire process took %d hours, %d minutes, and %d seconds'%(hours,mins,seconds))


def oneOnOne(player1,player2,n):
    toggle=True
    one=0
    two=0
    tie=0
    for i in range(n):
        global moveCounter
        moveCounter = 0
        gameStart = time.time()
        if toggle:
            winner, endType = checkersMain('', player1, player2)
        else:
            winner, endType = checkersMain('', player2, player1)
        moveCounter = 0
        if toggle:
            toggle = False
            if winner == 'r':
                one += 1
            elif winner == 'b':
                two += 1
            else:
                tie += 1
        else:
            toggle = True
            if winner == 'b':
                one += 1
            elif winner == 'r':
                two += 1
            else:
                tie += 1

        gameTime = time.time() - gameStart
        mins = gameTime // 60
        gameTime -= mins * 60
        print('The score is now',player1,':',one,player2,':',two,'Ties:', tie, 'Game',i+1)
        print('The game took %d minutes and %2.1f seconds, and ended for the reason: %s' % (mins, gameTime, endType))
    # print(player1,':',red,player2,':',black,'Tie:',tie)
    print('Time analysis:',player1, "took an average of %1.6f seconds per move, with %1.2f percent of moves that went 'overtime'" % (
    p1time[0] / p1time[1], p1time[2]/p1time[1]))
    print('Time analysis:',player2, "took an average of %1.6f seconds per move, with %1.2f percent of moves that went 'overtime'" % (
    p2time[0] / p2time[1], p2time[2]/p2time[1]))
    print('')
    print('')
    print('FINAL SCORE:   %s:%d   %s:%d   Ties:%d'%(player1,one,player2,two,tie))
    print('')
    print('')
def timeTrial(n):
    inFile = open('testSituation.txt', 'r')
    row = ["e", "e", "e", "e", "e", "e", "e", "e"]
    board = []
    for i in range(8):
        board.append(row[:])
    for rowIndex in range(8):
        line = inFile.readline()[:-1]
        for colIndex in range(8):
            if line[colIndex] in ["r", "b", "R", "B"]:
                board[rowIndex][colIndex] = line[colIndex]
    timeTot=0
    moves={}
    startTime = time.time()
    for i in range(n):
        move=Main.getValidMove(board,'r')
        if moves.get(move,-1)==-1:
            moves[move]=0
        moves[move]+=1
    print('Improved made a move of: %s Average time of: %1.2f seconds'%(move,(time.time()-startTime)/n))
    print(moves)
    moves={}

oneOnOne('P1','P2',50)
gameTime = time.time() - masterTime
hours = gameTime // 60**2
gameTime-=hours*60**2
mins = gameTime // 60
gameTime -= mins * 60
print('The game took %d hours %d minutes and %2.1f seconds' % (hours,mins, gameTime))