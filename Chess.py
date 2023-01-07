##TODO
# add blocking check mate checker
# add en-pessant movement to the pawns
# add pawn improvment mechanism

# bug list - 
# 


from abc import ABC, abstractmethod

class Game: #TODO
    def __init__(self):
        self.winner = None
        self.mates = None
        self.turn = 0

    def startGame(self): #TODO

        print("Welcome to my awosome chess game")
        player1 = input("White player, Please enter your name: ")
        player2 = input("Black player, Please enter your name: ")
        white = Player(player1,'W')
        black = Player(player2,'B')
        self.players = [white,black]
        
        
        self.board = Board()
        self.board.setBoard()
        print(self.board)

        while not self.winner:
            self.playTurn(self.players[self.turn%2])
            print(self.board)
            self.turn += 1
            
        

    def playTurn(self,player):
        piece = None
        target = None
        Enemy = self.players[(self.turn+1)%2]
                
        while not piece:
            
            finp = input(player.name + ", Choose a piece to move: ")
            f = self.getLocFromInput(finp)
            while not self.isValidLoc(f):
                print(f)
                finp = input("Invalid input, try again: ")
                f = self.getLocFromInput(finp)
                

            piece = self.board.onLoc(f)
            
            if not piece:
                print("square is empty, please choose one with a chess piece on it")
            elif not piece.availableMoves(self.board,f):
                print("This piece has nowhere to go, Choose a diffrent piece")
                piece = None
            elif piece.color != player.color:
                print("Thats the other's player piece silly, Choose a diffrent piece.")
                piece = None
        
        while not target:
            tinp = input("Choose a target square for the " + piece.type + ": ")
            target = self.getLocFromInput(tinp)
            if f == target or (not self.isValidLoc(target)) or (not piece.canMove(self.board,f,target)):
                print("Invalid target square, try again")
                target = None
        
        self.board.setSquare(f)
        self.board.setSquare(target,piece)
        
        if isinstance(piece,King):
            player.kingLoc = target
            
        if piece.matesKing(self.board,target,Enemy.kingLoc):
            self.mates = target
        return

    def getLocFromInput(self, inp): ## try to improve
        
        inp = inp.strip().upper()
        
        num = -1
        char = 'a'
        abc = ['A','B','C','D','E','F','G','H']

        for c in inp:
            if ord(c) <= ord('8') and ord(c) >= ord('1'):
                if num != -1:
                    return (-1,-1)
                num = int(c)
            elif c in abc:
                if char != 'a':
                    return (-1,-1)
                char = c
            elif not c.isspace():
                return (-1,-1)
        else:
            print((8-num,abc.index(char)))  ## DEL at end
            return (8-num,abc.index(char))

    def isValidLoc(self,loc):
        if Board.isOutOfBounds(loc):
            return False
        else:
            return True


class Board: #TODO

    def __init__(self):
        self.board = [[None]*8 for i in range(8)]

    def onLoc(self,loc):
        piece = self.board[loc[0]][loc[1]]
        if not piece:
            return None
        else:
            return piece

    def setBoard(self):
        for p in [0,7]:
            self.board[0][p] = Rook('B')
            self.board[7][p] = Rook('W')

        for p in [1,6]:
            self.board[0][p] = Knight('B')
            self.board[7][p] = Knight('W')
        
        for p in [2,5]:
            self.board[0][p] = Bishop('B')
            self.board[7][p] = Bishop('W')
        
        for p in range(8):
            self.board[1][p] = Pawn('B')
            self.board[6][p] = Pawn('W')

        self.board[0][3] = Queen('B')
        self.board[7][3] = Queen('W')

        self.board[0][4] = King('B')
        self.board[7][4] = King('W')

        return
    
    def setSquare(self,loc,piece=None):
        self.board[loc[0]][loc[1]] = piece
        return
    
    def isSquareThreatend(self,loc,color):
        ## by bishops and queens
        for i in [-1,1]:
            for j in [-1,1]:
                curloc = loc
                curSquare = None
                while not curSquare:
                    curloc = (curloc[0]+i,curloc[1]+j)
                    if Board.isOutOfBounds(curloc):
                        break
                    curSquare = self.onLoc(curloc)
                if isinstance(curSquare,(Bishop,Queen)) and color != curSquare.color:
                    return True

        ## by rooks and queens
        for i in [-1,1]:
            for j in range(2):
                curloc = loc
                curSquare = None
                while not curSquare:
                    curloc = (curloc[0]+i*j,curloc[1]+i*((j+1)%2))
                    if Board.isOutOfBounds(curloc):
                            break
                    curSquare = self.onLoc(curloc)
                if isinstance(curSquare,(Rook,Queen)) and color != curSquare.color:
                    return True
            
        ## by knights
        threats = Knight.getMoves(loc)
        for threat in threats:
            if not Board.isOutOfBounds(threat):
                curSquare = self.onLoc(threat)
                if isinstance(curSquare,Knight) and color != curSquare.color:
                    return True
        
        ## by pawns
        if color == 'W':
            derection = 1
        else:
            derection = -1
        threats = [(loc[0]+derection,loc[1]+i) for i in [-1,1]]
        for threat in threats:
            if not Board.isOutOfBounds(threat):
                curSquare = self.onLoc(threat)
                if isinstance(curSquare,Pawn) and color != curSquare.color:
                    return True
                
        ## by the king
        for i in range(-1,2):
            for j in range(-1,2):
                curloc = (loc[0]+i,loc[1]+j)
                if not Board.isOutOfBounds(curloc):
                    curSquare = self.onLoc(curloc)
                    if isinstance(curSquare,Pawn) and color != curSquare.color:
                        return True

        return False
        
        
    def isOutOfBounds(loc):
        return loc[0] < 0 or loc[0] > 7 or loc[1] < 0 or loc[1] > 7
                
    def __str__(self): ## try to improve
        print("   A  B  C  D  E  F  G  H")
        s = "  " + "_"*24 + '\n'
        for i in range(8):                  ## for each row
            s += str(8-i)
            s += '|'
            for j in range(8):              ## for each col
                piece = self.onLoc((i,j))
                if not piece:
                    s += '  '
                else:
                    s += str(piece)
                s += '|'
            s += '\n'
            s += "  " + "-"*24 + '\n'
        return s


class Player: #TODO
    
    def __init__(self,name,color):
        self.name = name
        self.color = color
        if color == 'W':
            self.kingLoc = (7,4)
        else:
            self.kingLoc = (0,4)

class Piece(ABC): #TODO

    def __init__(self,color):
        self.color = color

    @abstractmethod
    def availableMoves(self,board,f):
        pass

    def availableMoves(self,board,f,moves):
        moves = self.removeOutOfBounds(moves)
        for move in moves:
            if not board.onLoc(move):
                return True
        return False

    def canMove(self,board,f,t):
        if not self.validMove(board,f,t):
            return False
        if self.wayBlocked(board,f,t):
            return False
        return True

    @abstractmethod
    def validMove(self,board,f,t):
        pass
    
    def wayBlocked(self,board,f,t):

        ## returns False diffrent piece on the way to target
        if f[0] < t[0]:
            vertiMove = 1
        elif f[0] > t[0]:
            vertiMove = -1
        else:
            vertiMove = 0

        if f[1] < t[1]:
            horizMove = 1
        elif f[1] > t[1]:
            horizMove = -1
        else:
            horizMove = 0

        fx = f[0] + vertiMove
        fy = f[1] + horizMove
        while (fx,fy) != t:                          ## blocking piece

            if board.onLoc((fx,fy)):
                return True

            fx += vertiMove
            fy += horizMove
            
        if board.onLoc(t) and board.onLoc(t).color == self.color: ## can't eat yourself
            return False    
        
        return False

    def matesKing(self,board,loc,enemyKingLoc):
        if self.canMove(board,loc,enemyKingLoc):
            return True
        else:
            return False
    
    def removeOutOfBounds(self,moves):
        newMoves = [move for move in moves if not Board.isOutOfBounds(move)]
        return newMoves

class Rook(Piece): #TODO
    
    def __init__(self,color):
        super().__init__(color)
        self.type = "Rook"
    
    def availableMoves(self,board,f):
        moves = [(f[0]+i,f[1]+j) for i in range(-1,2) for j in range(-1,2)
                 if i == 0 or j == 0]
        return super().availableMoves(board,f,moves)


    def validMove(self,board,f,t):
        return f[0] == t[0] or f[1] == t[1]
    
    def __str__(self):
        if self.color == 'W':
            return "♖ "
        else:
            return "♜ "

class Knight(Piece):

    def __init__(self,color):
        super().__init__(color)
        self.type = "Knight"
    
    def availableMoves(self,board,f):
        moves = Knight.getMoves(f)    
        return super().availableMoves(board,f,moves)

    def validMove(self,board,f,t):
        moves = Knight.getMoves(f)
        return t in moves
    
    def wayBlocked(self,board,f,t):
        if board.onLoc(t) and board.onLoc(t).color == self.color:
            return False
        else:
            return True
        
    def getMoves(loc):
        return [(loc[0]+1,loc[1]+2),(loc[0]-1,loc[1]+2),(loc[0]-1,loc[1]-2),(loc[0]+1,loc[1]-2),
                 (loc[0]+2,loc[1]+1),(loc[0]-2,loc[1]+1),(loc[0]-2,loc[1]-1),(loc[0]+2,loc[1]-1) ]

    def __str__(self):
        if self.color == 'W':
            return "♘ "
        else:
            return "♞ "

class Bishop(Piece):

    def __init__(self,color):
        super().__init__(color)
        self.type = "Bishop"

    def availableMoves(self,board,f):
        moves = [(f[0]+i,f[1]+j) for i in [-1,1] for j in [-1,1]]
        return super().availableMoves(board,f,moves)

    def validMove(self, board, f, t):
        A = [(f[0]+i,f[1]+i) for i in range(1,7) if (f[0]+i<8 and f[1]+i<8)]
        B = [(f[0]-i,f[1]+i) for i in range(1,7) if (f[0]+i>=0 and f[1]+i<8)]
        C = [(f[0]-i,f[1]-i) for i in range(1,7) if (f[0]+i>=0 and f[1]+i>=0)]
        D = [(f[0]+i,f[1]-i) for i in range(1,7) if (f[0]+i<8 and f[1]+i>=0)]

        if t in A+B+C+D:
            return True
        else:
            return False
        

    def __str__(self):
        if self.color == 'W':
            return "♗ "
        else:
            return "♝ "

class Pawn(Piece):
    def __init__(self,color):
        super().__init__(color)
        self.type = "Pawn"

    def availableMoves(self,board,f):
        derection = self.getDerection()
        moves = [(f[0]+derection,f[1])]
        if (f[1] < 7 and board.onLoc((f[0] + derection,f[1]+1))) and board.onLoc((f[0] + derection,f[1]+1)).color != self.color:
            return True
        if (f[1] > 0 and board.onLoc((f[0] + derection,f[1]-1))) and board.onLoc((f[0] + derection,f[1]-1)) != self.color:
            return True
        return super().availableMoves(board,f,moves)

    def validMove(self,board, f, t):

        derection = self.getDerection()
        if t[1] == f[1] and t[0] == f[0] + derection and not board.onLoc(t): ## simple movement
            return True

        elif t[1] == f[1] and f[0] == (3.5-derection*2.5) and t[0] == f[0] + derection*2: ## from the starting line, a pawn can move forward twice
            return True

        elif t[0] == f[0] + derection and (t[1] == f[1]-1 or t[1] == f[1]+1) and board.onLoc(t): ## a pawn can eat enemie's pieces diagonaly
            return True
        
        ## if movement bellow not clear, Google en passant
        ## TODO
    
    def getDerection(self):
        if self.color == 'W':
            derection = -1
        else:
            derection = 1

        return derection

    def __str__(self):
        if self.color == 'W':
            return "♙ "
        else:
            return "♟ "

class Queen(Piece):
    def __init__(self,color):
        super().__init__(color)
        self.type = "Queen"

    def availableMoves(self,board,f):
        
        moves = [(f[0]+i,f[1]+j) for i in range(-1,2) for j in range(-1,2)]
        return super().availableMoves(board,f,moves)
        
    def validMove(self,board, f, t):
        return Rook.validMove(self,board,f,t) or Bishop.validMove(self,board,f,t)


    def __str__(self):
        if self.color == 'W':
            return "♕ "
        else:
            return "♛ "

class King(Piece):
    def __init__(self,color):
        super().__init__(color)
        self.type = "King"
    
    def availableMoves(self,board,f):
        moves =  self.getMoves(board,f)
        return super().availableMoves(board,f,moves)

    def validMove(self, board, f, t):
        moves = self.getMoves(board,f)
        if t in moves:
            return True
        else:
            return False

    def getMoves(self,board,f):
        return [(f[0]+i,f[1]+j) for i in range(-1,2) for j in range(-1,2)
                if not board.isSquareThreatend((f[0]+i,f[1]+j),self.color)]

    def __str__(self):
        if self.color == 'W':
            return "♔ "
        else:
            return "♚ "



g = Game()
g.startGame()