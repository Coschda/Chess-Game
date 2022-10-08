from errors import BadMoveError, TwoPossibleError, VraimentBizarre

'''
        self.board = [
    [Rook(0,0,"B"),Knight(0,1,"B"),Bishop(0,2,"B"),Queen(0,3,"B"),King(0,4,"B"),Bishop(0,5,"B"),Knight(0,6,"B"),Rook(0,7,"B")],
    [Pawn(1,0,"B"),Pawn(1,1,"B"),Pawn(1,2,"B"),Pawn(1,3,"B"),Pawn(1,4,"B"),Pawn(1,5,"B"),Pawn(1,6,"B"),Pawn(1,7,"B")],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [Pawn(6,0,"W"),Pawn(6,1,"W"),Pawn(6,2,"W"),Pawn(6,3,"W"),Pawn(6,4,"W"),Pawn(6,5,"W"),Pawn(6,6,"W"),Pawn(6,7,"W")],
    [Rook(7,0,"W"),Knight(7,1,"W"),Bishop(7,2,"W"),Queen(7,3,"W"),King(7,4,"W"),Bishop(7,5,"W"),Knight(7,6,"W"),Rook(7,7,"W")]
]

LISTE : abcdefgh BRNQK

Moves templates:
    - Pawn : e6 b4 a3
    - Knight : Nf3 Na4
    - Bishop : Be2 Be7
    - Rook : Rg8 Ra8
    - Queen : Qe1 Qd6
    - King : Ke2 Ke7

    - Roc : O-O O-O-O
    - Take : Nxe5 Qxe5 Bxg4

len(move)==2 : C'est un pion.
move[-2:] : case où l'action se passe.
'''

l2nb = {
    "a" : 0,
    "b" : 1,
    "c" : 2,
    "d" : 3,
    "e" : 4,
    "f" : 5,
    "g" : 6,
    "h" : 7
}

#Si commence par maj alors pièce majeure

def move2ind(move):
    try:
        x = l2nb[move[-2]]
        y = 8-int(move[-1])
        return (x, y)
    except:
        raise BadMoveError

def getcolpion(board, col, piece):
    pion = []
    for i in range(len(board.board)):
        ctx = board.board[i][col]
        if ctx != 0:
            if ctx.color==board.turn and type(ctx) == piece:
                pion.append(ctx)
    return pion

def movecheck(board, coo_move, jlist):
    if len(jlist)>1:
        raise TwoPossibleError
    elif len(jlist)==1:
        pion = jlist[0]
        board[coo_move[1]][coo_move[0]]=pion
        board[pion.y][pion.x] = 0
        pion.x, pion.y = coo_move
        return
    elif len(jlist)==0:
        raise BadMoveError

def cheathonte2(board, piece, coo_move, color):
    jlist = []
    for i in board:
        for j in i:
            if type(j)==piece:
                if j.color == color:
                    if j.peutbouger(board,move):
                        jlist.append(j)
    movecheck(board, coo_move, jlist)

class Piece:
    def __init__(self, y, x, color):
        self.y = y
        self.x = x
        self.color=color

class Pawn(Piece):
    def peutbouger(self, board, move):
        x, y = move2ind(move)
        distance = x-self.x  
        ecart = y-self.y      
        if self.color=="W":
            if distance == 0: #Sur la même colonne
                if ecart == -1:
                    if board[self.y-1][self.x]==0:
                        return True

                elif ecart == -2:
                    if self.y==6 and board[self.y-1][self.x]==0 and board[self.y-2][self.x]==0:
                        return True
                return False

            elif distance == 1: #Une colonne d'écart
                if ecart == -1 and board[self.y-1][self.x+1]!=self.color:
                    return True
                return False

            elif distance == -1:
                if ecart == -1 and board[self.y-1][self.x-1]!=self.color:
                    return True
                return False

            return False
        else:
            if distance==0: #Sur la même colonne
                if ecart == 1:
                    if board[self.y+1][self.x] == 0:
                        return True

                elif ecart == 2:
                    if self.y==1 and board[self.y+1][self.x]==0 and board[self.y+2][self.x]==0:
                        return True
                return False

            elif distance == 1: #Une colonne d'écart
                if ecart == 1 and board[self.y+1][self.x+1]!=self.color:
                    return True
                return False

            elif distance == -1:
                if ecart == 1 and board[self.y+1][self.x-1]!=self.color:
                    return True
                return False
            return False

    def __str__(self):
        if self.color=="W":
            return "♙"
        else:
            return "♟"

class Knight(Piece):
    def peutbouger(self, board, move):
        x, y = move2ind(move)
        distance = x-self.x
        ecart = y-self.y 

        if abs(distance)+abs(ecart)==3 and distance!=0 and ecart!=0:
            if board[y][x]==0:
                return True
            elif board[y][x].color != self.color:
                return True
            return False
        return False

    def __str__(self):
        if self.color=="W":
            return "♘"
        else:
            return "♞"

class Bishop(Piece):
    def peutbouger(self, board, move):
        x, y = move2ind(move)
        distance = x-self.x
        ecart = y-self.y
        comp = 0

        if abs(distance) == abs(ecart):
            i_x, i_y = self.x, self.y
            if ecart+distance >0:
                
                while i_x!=x and i_y!=y:
                    i_x+=1
                    i_y+=1

                    if board[i_y][i_x]!=0:
                        comp+=1
                        if comp==2:
                            return False
                        elif i_x == x and i_y == y and board[y][x].color != self.color:
                            return True
                        else:
                            return False
                return True
            
                

            elif ecart+distance <0:

                while i_x!=x and i_y!=y:
                    i_x-=1
                    i_y-=1

                    if board[i_y][i_x]!=0:
                        comp+=1
                        if comp==2:
                            return False
                        elif i_x == x and i_y == y and board[y][x].color != self.color:
                            return True
                        else:
                            return False
                return True

            elif ecart+distance == 0:
                if distance>0:

                    while i_x!=x and i_y!=y:
                        i_x+=1
                        i_y-=1

                        if board[i_y][i_x]!=0:
                            comp+=1
                            if comp==2:
                                return False
                            elif i_x == x and i_y == y and board[y][x].color != self.color:
                                return True
                            else:
                                return False
                    return True

                elif distance<0:

                    while i_x!=x and i_y!=y:
                        i_x-=1
                        i_y+=1

                        if board[i_y][i_x]!=0:
                            comp+=1
                            if comp==2:
                                return False
                            elif i_x == x and i_y == y and board[y][x].color != self.color:
                                return True
                            else:
                                return False
                    return True

                else:
                    return False

            else:
                return False
        else:
            return False

    def __str__(self):
        if self.color=="W":
            return "♗"
        else:
            return "♝"

class Rook(Piece):
    def peutbouger(self,board,move):
        x, y = move2ind(move)
        distance = x-self.x
        ecart = y-self.y
        comp = 0

        if distance == 0:
            if ecart > 0:
                i = self.y+1
                while i!=y+1:
                    if board[i][x]!=0:
                        comp+=1
                        if comp==2:
                            return False
                        elif i==y and board[i][x].color!=self.color:
                            return True
                        else:
                            return False
                    i+=1
                return True

            elif ecart < 0:
                
                i = self.y-1
                while i!=y-1:
                    if board[i][x]!=0:
                        comp+=1
                        if comp==2:
                            return False
                        elif i==y and board[i][x].color != self.color:
                            return True
                        else:
                            return False
                    i-=1
                return True
                    
        elif ecart == 0:
            if distance > 0:
                i = self.x+1
                while i!=x+1:
                    if board[y][i]!=0:
                        comp+=1
                        if comp==2:
                            return False
                        elif i==x and board[y][i].color != self.color:
                            return True
                        else:
                            return False
                    i+=1
                return True
            elif distance < 0:
                i = self.x-1
                while i!=x-1:
                    if board[y][i]!=0:
                        comp+=1
                        if comp==2:
                            return False
                        elif i==x and board[y][i].color != self.color:
                            return True
                        else:
                            return False
                    i-=1
                return True
        return False

        
    def __str__(self):
        if self.color=="W":
            return "♖"
        else:
            return "♜"

class Queen(Piece):
    def peutbouger(self, board, move):
        x, y = move2ind(move)
        distance = x-self.x
        ecart = y-self.y

        #FOU
        if abs(distance)==abs(ecart):
            return Bishop.peutbouger(self,board, move)

        #TOUR
        elif distance==0 or ecart==0:
            return Rook.peutbouger(self,board, move)

    def __str__(self):
        if self.color=="W":
            return "♕"
        else:
            return "♛"

class King(Piece):
    def peutbouger(self, board, move):
        x, y = move2ind(move)
        distance = x-self.x
        ecart = y-self.y

        if est_protege(board,move,"W" if self.color=="B" else "B"):
            return False
        if abs(ecart)+abs(distance) == 1 or (abs(distance) == 1 and abs(ecart) == 1):
            if board[y][x] == 0:
                return True
            elif board[y][x].color != self.color:
                return True
            else:
                return False
        raise VraimentBizarre

    def __str__(self):
        if self.color=="W":
            return "♔"
        else:
            return "♚"

def Naround(board, move, color):
    """Renvoie la liste des cavaliers autour d'une case avec le mouvement du cavalier de la couleur donnée."""
    coo_move = move2ind(move[-2:])
    liste_dist = [(2,1),(1,2),(-2,1),(-1,2),(2,-1),(1,-2),(-2,-1),(-1,-2)]
    klist = []
    for i in liste_dist:
        x = i[0]+coo_move[0]
        y = i[1]+coo_move[1]
        if x<=7 and y<=7:
            piece = board[y][x]
            if type(piece) == Knight and x>=0 and y>=0:
                if piece.color == color:
                    klist.append(piece)
    return klist

def getdia(board,move):
    x,y = move2ind(move)
    lis = []
    taille = len(board)-1

    signes = [('-','-'),('-','+'),('+','-'),('+','+')]
    for i in signes:
        x_i = eval(str(x)+f"{i[0]}1")
        y_i = eval(str(y)+f"{i[1]}1")
        while 0<=x_i<=taille and 0<=y_i<=taille:
            piece = board[y_i][x_i]
            if piece!=0:
                lis.append(piece)
                break
            else:
                lis.append(piece)
                x_i=eval(str(x_i)+f"{i[0]}1")
                y_i=eval(str(y_i)+f"{i[1]}1")
    return lis

def getrook(liste,move, color):
    x,y = move2ind(move)

    x_i = x+1
    y_i = y
    while 0<=x_i<=len(liste)-1 and 0<=y_i<=len(liste)-1:
        piece = liste[y_i][x_i]
        if piece!=0:
            if type(piece)==Rook or type(piece)==Queen:
                if piece.color == color:
                    return True
                else:
                    break
            else:
                break
        x_i+=1

    x_i = x-1
    y_i = y
    while 0<=x_i<=len(liste)-1 and 0<=y_i<=len(liste)-1:
        piece = liste[y_i][x_i]
        if piece!=0:
            if type(piece)==Rook or type(piece)==Queen:
                if piece.color == color:
                    return True
                else:
                    break
            else:
                break
        x_i-=1

    x_i = x
    y_i = y+1
    while 0<=x_i<=len(liste)-1 and 0<=y_i<=len(liste)-1:
        piece = liste[y_i][x_i]
        if piece!=0:
            if type(piece)==Rook or type(piece)==Queen:
                if piece.color == color:
                    return True
                else:
                    break
            else:
                break
        y_i+=1

    x_i = x
    y_i = y-1
    while 0<=x_i<=len(liste)-1 and 0<=y_i<=len(liste)-1:
        piece = liste[y_i][x_i]
        if piece!=0:
            if type(piece)==Rook or type(piece)==Queen:
                if piece.color == color:
                    return True
                else:
                    break
            else:
                break
        y_i-=1

    return False

def est_protege(board, move, color):
    """Bool de si la case est protégée PAR la couleur donnée."""
    if color == 'W':
        #Pion
        x,y = move2ind(move)
        if 1<=x<=len(board[0])-1 and 0<=y<=len(board[0])-2:
            pawn1 = board[y+1][x-1]
            if type(pawn1) ==Pawn:
                if pawn1.color == color:
                    return True

        if 0<=x<=len(board[0])-2 and 0<=y<=len(board[0])-2:
            pawn2 = board[y+1][x+1]
            if type(pawn2) == Pawn:
                if pawn2.color == color:
                    return True

    else:
        x,y = move2ind(move)
        if 1<=x<=len(board[0])-1 and 1<=y<=len(board[0])-1:
            pawn1 = board[y-1][x-1]
            if type(pawn1) ==Pawn:
                if pawn1.color == color:
                    return True

        if 0<=x<=len(board[0])-2 and 1<=y<=len(board[0])-1:
            pawn2 = board[y-1][x+1]
            if type(pawn2) == Pawn:
                if pawn2.color == color:
                    return True

    #Knight
    if Naround(board, move, color):
        return True

    #Bishop
    for i in getdia(board, move):
        if type(i)==Bishop or type(i)==Queen:
            if i.color==color:
                return True

    
    #King
    try:
        coo_x,coo_y = move2ind(move)
        if [board[coo_y+x[0]][coo_x+x[1]] for x in [x for x in [(-1,-1),(-1,0),(0,-1),(-1,+1),(+1,-1),(+1,0),(0,+1),(+1,+1)] if 0<=coo_y+x[0]<=7 and 0<=coo_x+x[1]<=7] if type(board[coo_y+x[0]][coo_x+x[1]])==King][0].color == color: return True
    except IndexError:
        pass

    #Rook
    return getrook(board,move,color)

class Board:
    def __init__(self):
        self.board = [
    [Rook(0,0,"B"),0,0,0,King(0,4,"B"),0,0,Rook(0,7,"B")],
    [Pawn(1,0,"B"),Pawn(1,1,"B"),Pawn(1,2,"B"),Pawn(1,3,"B"),Pawn(1,4,"B"),Pawn(1,5,"B"),Pawn(1,6,"B"),Pawn(1,7,"B")],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [Pawn(6,0,"W"),Pawn(6,1,"W"),Pawn(6,2,"W"),Pawn(6,3,"W"),Pawn(6,4,"W"),Pawn(6,5,"W"),Pawn(6,6,"W"),Pawn(6,7,"W")],
    [Rook(7,0,"W"),0,0,0,King(7,4,"W"),0,0,Rook(7,7,"W")]
]
        self.turn = "W"
        self.w_proc = True
        self.w_groc = True
        self.b_proc = True
        self.b_groc = True
    def __str__(self):
        txt = ""
        for i in self.board:
            for y in i:
                if y==0:
                    txt+= "  | "
                else:
                    txt += str(y)+" | "
            txt+="\n"
            txt+= "-------------------------------"
            txt+="\n"
        return txt

    def move(self, move:str, color):
        if len(move) == 2: #Pion qui avance
            coo_move = move2ind(move)
            #get le pion sur la colonne de la couleur du tour
            pion = getcolpion(self, coo_move[0], Pawn)
            
            #faire le move
            for i in pion:
                if i.peutbouger(self.board, move) and i.color == color:
                    self.board[coo_move[1]][coo_move[0]] = i
                    self.board[i.y][i.x] = 0
                    i.x, i.y = coo_move

        elif len(move)==3:
            if move[0].lower() == "n":
                coo_move = move2ind(move[-2:])
                klist = Naround(self.board, move, color)
                movecheck(self.board, coo_move, klist)

            elif move[0] == "B":
                coo_move = move2ind(move[-2:])
                cheathonte2(self.board, Bishop, coo_move, color)
            
            elif move[0].lower() == "r":
                coo_move = move2ind(move[-2:])
                cheathonte2(self.board, Rook, coo_move, color)

            elif move[0].lower() == "q":
                coo_move = move2ind(move[-2:])
                cheathonte2(self.board, Queen, coo_move, color)
            
            elif move[0].lower() == "k":
                coo_move = move2ind(move[-2:])
                cheathonte2(self.board, King, coo_move, color)
                if color == "W":
                    self.w_proc = False
                    self.w_groc = False
                else:
                    self.b_proc = False
                    self.b_groc = False

            elif move.lower()=="o-o" or move=="0-0":
                if color == "W" and self.w_proc and type(self.board[7][4])==King and type(self.board[7][7])==Rook:
                    if self.board[7][5]==0 and self.board[7][6]==0:
                        if est_protege(self.board, "f1", "B")==False and est_protege(self.board, "g1", "B")==False:

                            self.board[7][6], self.board[7][4] = self.board[7][4], self.board[7][6]
                            self.board[7][6].x,self.board[7][6].y = 6,7

                            self.board[7][7], self.board[7][5] = self.board[7][5], self.board[7][7]
                            self.board[7][5].x,self.board[7][5].y = 5,7

                            self.w_proc = False
                            self.w_groc = False

                elif color == "B" and self.b_proc and type(self.board[0][4])==King and type(self.board[0][7])==Rook:
                    if self.board[0][5]==0 and self.board[0][6]==0:
                        if est_protege(self.board, "f8", "W")==False and est_protege(self.board, "g8", "W")==False:

                            self.board[0][6], self.board[0][4] = self.board[0][4], self.board[0][6]
                            self.board[0][6].x,self.board[0][6].y = 6,0

                            self.board[0][7], self.board[0][5] = self.board[0][5], self.board[0][7]
                            self.board[0][5].x,self.board[0][5].y = 5,0

                            self.b_proc = False
                            self.b_groc = False

        elif len(move)==4: #Take Take Take
            coo_move = move2ind(move[-2:])

            if move[0].islower(): #C'est un pion qui prend
                #get le pion sur la colone...
                pion = getcolpion(self, l2nb[move[0]], Pawn)

                #faire le move
                for i in pion:
                    if i.peutbouger(self.board, move[2:]):
                        self.board[coo_move[1]][coo_move[0]] = i
                        self.board[i.y][i.x] = 0
                        i.x, i.y = coo_move

            else: #Piece Majeure prend
                if move[0].lower()=="n":
                    klist = Naround(self.board, move, color)
                    movecheck(self.board, coo_move, klist)
                
                elif move[0] == "B":
                    cheathonte2(self.board, Bishop, coo_move, color)

                elif move[0].lower() == "r":
                    cheathonte2(self.board, Rook, coo_move, color)

                elif move[0].lower() == "q":
                    cheathonte2(self.board, Queen, coo_move, color)

                elif move[0].lower() == "k":
                    cheathonte2(self.board, King, coo_move, color)

        elif len(move)==5:
            if move.lower()=="o-o-o" or move=="0-0-0":
                if color == "W" and self.w_groc and type(self.board[7][4])==King and type(self.board[7][0])==Rook:
                    if self.board[7][1]==0 and self.board[7][2]==0 and self.board[7][3]==0:
                        if est_protege(self.board, "b1", "B")==False and est_protege(self.board, "c1", "B")==False and est_protege(self.board, "d1", "B")==False:

                            self.board[7][2], self.board[7][4] = self.board[7][4], self.board[7][2]
                            self.board[7][2].x,self.board[7][2].y = 2,7

                            self.board[7][0], self.board[7][3] = self.board[7][3], self.board[7][0]
                            self.board[7][3].x,self.board[7][3].y = 3,7

                            self.w_groc = False

                elif color == "B" and self.b_groc and type(self.board[0][4])==King and type(self.board[0][0])==Rook:
                    if self.board[0][1]==0 and self.board[0][2]==0 and self.board[0][3]==0:
                        if est_protege(self.board, "b8", "W")==False and est_protege(self.board, "c8", "W")==False and est_protege(self.board, "d8", "W")==False:

                            self.board[0][2], self.board[0][4] = self.board[0][4], self.board[0][2]
                            self.board[0][2].x,self.board[0][2].y = 2,0

                            self.board[0][0], self.board[0][3] = self.board[0][3], self.board[0][0]
                            self.board[0][3].x,self.board[0][3].y = 3,0

                            self.b_groc = False



if __name__ == "__main__":

    a = Board()

    comp = 0
    while True:
        if comp%2==0:
            a.turn = "W"
        else:
            a.turn = "B"
        print(a)
        print(a.turn)
        move = input("Faites un move : ")
        ancien_board = a.board
        a.move(move,a.turn)

        comp+=1