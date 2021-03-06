# pieces.py

import pygame
pygame.init()

pygame.display.set_mode((800, 800))

pieces = pygame.image.load("Images\Pieces.png")  # spritesheet of all pieces
piece_images = {}

w_pawn = pieces.subsurface((1750, 10, 332, 340))
piece_images['w_pawn'] = pygame.transform.scale(w_pawn, (96, 96)).convert_alpha()
b_pawn = pieces.subsurface((1750, 350, 332, 340))
piece_images['b_pawn'] = pygame.transform.scale(b_pawn, (96, 96)).convert_alpha()
w_bishop = pieces.subsurface((703, 0, 340, 340))
piece_images['w_bishop'] = pygame.transform.scale(w_bishop, (96, 96)).convert_alpha()
b_bishop = pieces.subsurface((703, 350, 340, 340))
piece_images['b_bishop'] = pygame.transform.scale(b_bishop, (96, 96)).convert_alpha()
w_knight = pieces.subsurface((1050, 0, 340, 340))
piece_images['w_knight'] = pygame.transform.scale(w_knight, (96, 96)).convert_alpha()
b_knight = pieces.subsurface((1050, 350, 340, 340))
piece_images['b_knight'] = pygame.transform.scale(b_knight, (96, 96)).convert_alpha()
w_rook = pieces.subsurface((1400, 0, 340, 340))
piece_images['w_rook'] = pygame.transform.scale(w_rook, (96, 96)).convert_alpha()
b_rook = pieces.subsurface((1400, 350, 340, 340))
piece_images['b_rook'] = pygame.transform.scale(b_rook, (96, 96)).convert_alpha()
w_queen = pieces.subsurface((355, 0, 340, 340))
piece_images['w_queen'] = pygame.transform.scale(w_queen, (96, 96)).convert_alpha()
b_queen = pieces.subsurface((355, 350, 340, 340))
piece_images['b_queen'] = pygame.transform.scale(b_queen, (96, 96)).convert_alpha()
w_king = pieces.subsurface((5, 0, 340, 340))
piece_images['w_king'] = pygame.transform.scale(w_king, (96, 96)).convert_alpha()
b_king = pieces.subsurface((5, 350, 340, 340))
piece_images['b_king'] = pygame.transform.scale(b_king, (96, 96)).convert_alpha()


# square names matched to their cords, now with 2 dicts for both sides
squares_black = {}
squares_white = {}
for i in range(1, 9):
    for j, file in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
        squares_white[file + str(i)] = (16 + 96*j, 800 - 16 - 96*i)
        squares_black[file + str(i)] = (800 - 16 - 96*(j+1), 16 + 96*(i-1))


# sounds
move = pygame.mixer.Sound("Sounds\Move.wav")
capture = pygame.mixer.Sound("Sounds\Capture.wav")


class Piece(object):
    '''
    Parent class for all piece types
    '''

    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.state = 'Down'  # 'Down' 'Lifted' or 'Selected'
        self.cords = (0, 0)

    def draw(self, screen, outline, piece_list, occupied, player):
        if player == 'White':
            squares = squares_white
        else:  # if player == 'Black'
            squares = squares_black
        if self.state == 'Down':
            screen.blit(piece_images[self.image], squares[self.position])
        elif self.state == 'Selected':
            screen.blit(piece_images[self.image], squares[self.position])
            screen.blit(outline, squares[self.position])
            for sq in self.legal_moves(piece_list, occupied):
                screen.blit(outline, squares[sq])
        elif self.state == 'Lifted':
            for sq in self.legal_moves(piece_list, occupied):
                screen.blit(outline, squares[sq])
            screen.blit(piece_images[self.image], self.cords)

    def move(self, dest, piece_list, occupied):
        if occupied[dest] is None:
            move.play()
        else:
            capture.play()
            piece_list.remove(occupied[dest])
            occupied[dest] = self

        occupied[self.position] = None
        self.position = dest
        occupied[self.position] = self
        self.state = 'Down'

    def move_capture(self, dest, piece_list, occupied):
        '''
        Returns the captured piece in a possible move
        '''
        if occupied[dest] is not None:
            captured = occupied[dest]
            piece_list.remove(occupied[dest])
            occupied[dest] = self

        occupied[self.position] = None
        self.position = dest
        occupied[self.position] = self
        return captured


class Pawn(Piece):

    def __init__(self, colour, position):
        super(Pawn, self).__init__(colour, position)
        if colour == 'White':
            self.image = 'w_pawn'
        else:
            self.image = 'b_pawn'
        self.en_passant = False  # keep track if this move can be played onto this pawn

    def possible_captures(self):
        legal = []
        if self.colour == 'White':
            # check squares diagonal and infront to see if you can move by capturing
            legal.append(chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 1))
            legal.append(chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 1))
        elif self.colour == 'Black':
            # check squares diagonal and infront to see if you can move by capturing
            legal.append(chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 1))
            legal.append(chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 1))

        return legal

    def legal_moves(self, piece_list, occupied):
        '''
        Returns a list of squares a piece can move to
        '''
        legal = []
        if self.colour == 'White':
            if occupied[self.position[0] + str(int(self.position[1]) + 1)] is None:
                legal.append(self.position[0] + str(int(self.position[1]) + 1))
                # check if pawn is on starting square, if so it can move 2 squares forward
                if self.position[1] == '2' and occupied[self.position[0] + str(int(self.position[1]) + 2)] == None:
                    legal.append(self.position[0] + str(int(self.position[1]) + 2))

        elif self.colour == 'Black':
            if occupied[self.position[0] + str(int(self.position[1]) - 1)] is None:
                legal.append(self.position[0] + str(int(self.position[1]) - 1))
                # check if pawn is on starting square, if so it can move 2 squares forward
                if self.position[1] == '7' and occupied[self.position[0] + str(int(self.position[1]) - 2)] == None:
                    legal.append(self.position[0] + str(int(self.position[1]) - 2))

        for dest in self.possible_captures():
            if dest in occupied and occupied[dest] != None and occupied[dest].colour != self.colour:
                legal.append(dest)

        # check en passant
        left = chr(ord(self.position[0]) - 1) + self.position[1]
        right = chr(ord(self.position[0]) + 1) + self.position[1]
        if (left in occupied and str(type(occupied[left])) == "<class 'pieces.Pawn'>" and occupied[left].en_passant == True):
            if self.colour == 'White':
                if occupied[chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 1)] == None:
                    legal.append(chr(ord(self.position[0]) - 1) + str(int(self.position[1]) + 1))
            else: # if colour is black
                if occupied[chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 1)] == None:
                    legal.append(chr(ord(self.position[0]) - 1) + str(int(self.position[1]) - 1))

        if (right in occupied and str(type(occupied[right])) == "<class 'pieces.Pawn'>" and occupied[right].en_passant == True):
            if self.colour == 'White':
                if occupied[chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 1)] == None:
                    legal.append(chr(ord(self.position[0]) + 1) + str(int(self.position[1]) + 1))
            else: # if colour is black
                if occupied[chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 1)] == None:
                    legal.append(chr(ord(self.position[0]) + 1) + str(int(self.position[1]) - 1))

        next_checker = []
        for sq in legal:
            original = self.position
            self.position = sq
            occupied[original] = None
            new = occupied[sq]
            occupied[sq] = self
            if new != None:
                piece_list.remove(new)
            for piece in piece_list:
                if str(type(piece)) == "<class 'pieces.King'>" and piece.colour == self.colour:
                    king = piece
            if not king.in_check(piece_list, occupied):
                next_checker.append(sq)
            self.position = original
            occupied[original] = self
            occupied[sq] = new
            if new != None:
                piece_list.append(new)

        return next_checker

    def attacking_squares(self, piece_list, occupied):
        '''
        Returns the squares the piece is attacking
        (Basically the legal moves func without checking the next move)
        '''
        legal = []
        if self.colour == 'White' and self.position[1] != '8':
            if occupied[self.position[0] + str(int(self.position[1]) + 1)] == None:
                legal.append(self.position[0] + str(int(self.position[1]) + 1))
                # check if pawn is on starting square, if so it can move 2 squares forward
                if self.position[1] == '2' and occupied[self.position[0] + str(int(self.position[1]) + 2)] == None:
                    legal.append(self.position[0] + str(int(self.position[1]) + 2))

        elif self.colour == 'Black' and self.position[1] != '1':
            if occupied[self.position[0] + str(int(self.position[1]) - 1)] == None:
                legal.append(self.position[0] + str(int(self.position[1]) - 1))
                # check if pawn is on starting square, if so it can move 2 squares forward
                if self.position[1] == '7' and occupied[self.position[0] + str(int(self.position[1]) - 2)] == None:
                    legal.append(self.position[0] + str(int(self.position[1]) - 2))

        for dest in self.possible_captures():
            if dest in occupied and occupied[dest] != None and occupied[dest].colour != self.colour:
                legal.append(dest)

        return legal

    def promote(self, piece_list, occupied):
        '''
        Check conditions of promotion and promotes as needed
        '''
        if (self.colour == 'White' and self.position[1] == '8') or (self.colour == 'Black' and self.position[1] == '1'):
            queen = Queen(self.colour, self.position)
            piece_list[piece_list.index(self)] = queen
            occupied[self.position] = queen

    def move(self, dest, piece_list, occupied):
        en_passant = False
        if occupied[dest] == None and self.position[0] != dest[0]:
            en_passant = True
        if occupied[dest] == None and en_passant == False:
            move.play()
        else:
            capture.play()
            if en_passant == False:
                piece_list.remove(occupied[dest])
            occupied[dest] = self

        if abs(int(self.position[1]) - int(dest[1])) == 2:
            self.en_passant = True
        else:
            self.en_passant = False

        occupied[self.position] = None
        self.position = dest
        occupied[self.position] = self
        self.state = 'Down'

        if en_passant:
            if self.colour == 'White':
                piece_list.remove(occupied[self.position[0] + str(int(self.position[1]) - 1)])
                occupied[self.position[0] + str(int(self.position[1]) - 1)] = None
            else: # if self.colour == 'Black':
                piece_list.remove(occupied[self.position[0] + str(int(self.position[1]) + 1)])
                occupied[self.position[0] + str(int(self.position[1]) + 1)] = None


class Bishop(Piece):

    def __init__(self, colour, position):
        super(Bishop, self).__init__(colour, position)
        if colour == 'White':
            self.image = 'w_bishop'
        else:
            self.image = 'b_bishop'

    def legal_moves(self, piece_list, occupied):
        '''
        Returns a list of squares a piece can move to
        '''
        legal = []
        diagonal = 1
        paths = [True, True, True, True] # top left, top right, bottom right, bottom left
        # checks all diagonals that are 'diagonal' units away from the position

        while True in paths:
            if paths[0]:
                sq = chr(ord(self.position[0]) - diagonal) + str(int(self.position[1]) + diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[0] = False
                else:
                    paths[0] = False
            if paths[1]:
                sq = chr(ord(self.position[0]) + diagonal) + str(int(self.position[1]) + diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[1] = False
                else:
                    paths[1] = False
            if paths[2]:
                sq = chr(ord(self.position[0]) + diagonal) + str(int(self.position[1]) - diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[2] = False
                else:
                    paths[2] = False
            if paths[3]:
                sq = chr(ord(self.position[0]) - diagonal) + str(int(self.position[1]) - diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[3] = False
                else:
                    paths[3] = False

            diagonal += 1

        next_checker = []
        for sq in legal:
            original = self.position
            self.position = sq
            occupied[original] = None
            new = occupied[sq]
            occupied[sq] = self
            if new != None:
                piece_list.remove(new)
            for piece in piece_list:
                if str(type(piece)) == "<class 'pieces.King'>" and piece.colour == self.colour:
                    king = piece
            if not king.in_check(piece_list, occupied):
                next_checker.append(sq)
            self.position = original
            occupied[original] = self
            occupied[sq] = new
            if new != None:
                piece_list.append(new)

        return next_checker

    def attacking_squares(self, piece_list, occupied):
        '''
        Returns the squares the piece is attacking
        (Basically the legal moves func without checking the next move)
        '''
        legal = []
        diagonal = 1
        paths = [True, True, True, True] # top left, top right, bottom right, bottom left
        # checks all diagonals that are 'diagonal' units away from the position

        while True in paths:
            if paths[0]:
                sq = chr(ord(self.position[0]) - diagonal) + str(int(self.position[1]) + diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[0] = False
                else:
                    paths[0] = False
            if paths[1]:
                sq = chr(ord(self.position[0]) + diagonal) + str(int(self.position[1]) + diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[1] = False
                else:
                    paths[1] = False
            if paths[2]:
                sq = chr(ord(self.position[0]) + diagonal) + str(int(self.position[1]) - diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[2] = False
                else:
                    paths[2] = False
            if paths[3]:
                sq = chr(ord(self.position[0]) - diagonal) + str(int(self.position[1]) - diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[3] = False
                else:
                    paths[3] = False

            diagonal += 1

        return legal


class Knight(Piece):

    def __init__(self, colour, position):
        super(Knight, self).__init__(colour, position)
        if colour == 'White':
            self.image = 'w_knight'
        else:
            self.image = 'b_knight'


    def legal_moves(self, piece_list, occupied):
        '''
        Returns a list of squares a piece can move to
        '''
        legal = []
        # manually check the 8 squares a knight could jump too
        for i in [1, -1]:
            for j in [1, -1]:
                dest = chr(ord(self.position[0]) + 2*i) + str(int(self.position[1]) + j)
                '''
                Checks these possible moves
                   ↔
                   |
                   K
                   |
                   ↔
                '''
                if dest in occupied and (occupied[dest] == None or occupied[dest].colour != self.colour):
                    legal.append(dest)

                dest = chr(ord(self.position[0]) + i) + str(int(self.position[1]) + 2*j)
                '''
                Checks these possible moves
                ↕ - K - ↕
                '''
                if dest in occupied and (occupied[dest] == None or occupied[dest].colour != self.colour):
                    legal.append(dest)

        next_checker = []
        for sq in legal:
            original = self.position
            self.position = sq
            occupied[original] = None
            new = occupied[sq]
            occupied[sq] = self
            if new != None:
                piece_list.remove(new)
            for piece in piece_list:
                if str(type(piece)) == "<class 'pieces.King'>" and piece.colour == self.colour:
                    king = piece
            if not king.in_check(piece_list, occupied):
                next_checker.append(sq)
            self.position = original
            occupied[original] = self
            occupied[sq] = new
            if new != None:
                piece_list.append(new)

        return next_checker


    def attacking_squares(self, piece_list, occupied):
        '''
        Returns the squares the piece is attacking
        (Basically the legal moves func without checking the next move)
        '''
        legal = []
        # manually check the 8 squares a knight could jump too
        for i in [1, -1]:
            for j in [1, -1]:
                dest = chr(ord(self.position[0]) + 2*i) + str(int(self.position[1]) + j)
                '''
                Checks these possible moves
                   ↔
                   |
                   K
                   |
                   ↔
                '''
                if dest in occupied and (occupied[dest] == None or occupied[dest].colour != self.colour):
                    legal.append(dest)

                dest = chr(ord(self.position[0]) + i) + str(int(self.position[1]) + 2*j)
                '''
                Checks these possible moves
                ↕ - K - ↕
                '''
                if dest in occupied and (occupied[dest] == None or occupied[dest].colour != self.colour):
                    legal.append(dest)


        return legal


class Rook(Piece):

    def __init__(self, colour, position):
        super(Rook, self).__init__(colour, position)
        self.has_moved = False # to keep track of castles
        if colour == 'White':
            self.image = 'w_rook'
        else:
            self.image = 'b_rook'


    def legal_moves(self, piece_list, occupied):
        '''
        Returns a list of squares a piece can move to
        '''
        legal = []
        # similar to the bishop's movement
        distance = 1
        paths = [True, True, True, True] # left, right, up, down

        while True in paths:
            if paths[0]:
                sq = chr(ord(self.position[0]) - distance) + self.position[1]
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[0] = False
                else:
                    paths[0] = False
            if paths[1]:
                sq = chr(ord(self.position[0]) + distance) + self.position[1]
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[1] = False
                else:
                    paths[1] = False
            if paths[2]:
                sq = self.position[0] + str(int(self.position[1]) + distance)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[2] = False
                else:
                    paths[2] = False
            if paths[3]:
                sq = self.position[0] + str(int(self.position[1]) - distance)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[3] = False
                else:
                    paths[3] = False

            distance += 1

        next_checker = []
        for sq in legal:
            original = self.position
            self.position = sq
            occupied[original] = None
            new = occupied[sq]
            occupied[sq] = self
            if new != None:
                piece_list.remove(new)
            for piece in piece_list:
                if str(type(piece)) == "<class 'pieces.King'>" and piece.colour == self.colour:
                    king = piece
            if not king.in_check(piece_list, occupied):
                next_checker.append(sq)
            self.position = original
            occupied[original] = self
            occupied[sq] = new
            if new != None:
                piece_list.append(new)

        return next_checker


    def attacking_squares(self, piece_list, occupied):
        '''
        Returns the squares the piece is attacking
        (Basically the legal moves func without checking the next move)
        '''
        legal = []
        # similar to the bishop's movement
        distance = 1
        paths = [True, True, True, True] # left, right, up, down

        while True in paths:
            if paths[0]:
                sq = chr(ord(self.position[0]) - distance) + self.position[1]
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[0] = False
                else:
                    paths[0] = False
            if paths[1]:
                sq = chr(ord(self.position[0]) + distance) + self.position[1]
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[1] = False
                else:
                    paths[1] = False
            if paths[2]:
                sq = self.position[0] + str(int(self.position[1]) + distance)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[2] = False
                else:
                    paths[2] = False
            if paths[3]:
                sq = self.position[0] + str(int(self.position[1]) - distance)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[3] = False
                else:
                    paths[3] = False

            distance += 1

        return legal


    def move(self, dest, piece_list, occupied):
        if occupied[dest] == None:
            move.play()
        else:
            capture.play()
            piece_list.remove(occupied[dest])
            occupied[dest] = self

        self.has_moved = True
        occupied[self.position] = None
        self.position = dest
        occupied[self.position] = self
        self.state = 'Down'


    def castle(self, occupied):
        occupied[self.position] = None
        if self.position[0] == 'a':
            self.position = 'd' + self.position[1]
        elif self.position[0] == 'h':
            self.position = 'f' + self.position[1]

        occupied[self.position] = self


class Queen(Piece):

    def __init__(self, colour, position):
        super(Queen, self).__init__(colour, position)
        if colour == 'White':
            self.image = 'w_queen'
        else:
            self.image = 'b_queen'


    def legal_moves(self, piece_list, occupied):
        '''
        Returns a list of squares a piece can move to
        '''
        legal = []
        # combine bishop and rook movement

        diagonal = 1
        paths = [True, True, True, True] # top left, top right, bottom right, bottom left
        # checks all diagonals that are 'diagonal' units away from the position

        while True in paths:
            if paths[0]:
                sq = chr(ord(self.position[0]) - diagonal) + str(int(self.position[1]) + diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[0] = False
                else:
                    paths[0] = False
            if paths[1]:
                sq = chr(ord(self.position[0]) + diagonal) + str(int(self.position[1]) + diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[1] = False
                else:
                    paths[1] = False
            if paths[2]:
                sq = chr(ord(self.position[0]) + diagonal) + str(int(self.position[1]) - diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[2] = False
                else:
                    paths[2] = False
            if paths[3]:
                sq = chr(ord(self.position[0]) - diagonal) + str(int(self.position[1]) - diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[3] = False
                else:
                    paths[3] = False

            diagonal += 1

        distance = 1
        paths = [True, True, True, True] # left, right, up, down

        while True in paths:
            if paths[0]:
                sq = chr(ord(self.position[0]) - distance) + self.position[1]
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[0] = False
                else:
                    paths[0] = False
            if paths[1]:
                sq = chr(ord(self.position[0]) + distance) + self.position[1]
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[1] = False
                else:
                    paths[1] = False
            if paths[2]:
                sq = self.position[0] + str(int(self.position[1]) + distance)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[2] = False
                else:
                    paths[2] = False
            if paths[3]:
                sq = self.position[0] + str(int(self.position[1]) - distance)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[3] = False
                else:
                    paths[3] = False

            distance += 1

        next_checker = []
        for sq in legal:
            original = self.position
            self.position = sq
            occupied[original] = None
            new = occupied[sq]
            occupied[sq] = self
            if new != None:
                piece_list.remove(new)
            for piece in piece_list:
                if str(type(piece)) == "<class 'pieces.King'>" and piece.colour == self.colour:
                    king = piece
            if not king.in_check(piece_list, occupied):
                next_checker.append(sq)
            self.position = original
            occupied[original] = self
            occupied[sq] = new
            if new != None:
                piece_list.append(new)
        return next_checker


    def attacking_squares(self, piece_list, occupied):
        '''
        Returns the squares the piece is attacking
        (Basically the legal moves func without checking the next move)
        '''
        legal = []
        # combine bishop and rook movement

        diagonal = 1
        paths = [True, True, True, True] # top left, top right, bottom right, bottom left
        # checks all diagonals that are 'diagonal' units away from the position

        while True in paths:
            if paths[0]:
                sq = chr(ord(self.position[0]) - diagonal) + str(int(self.position[1]) + diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[0] = False
                else:
                    paths[0] = False
            if paths[1]:
                sq = chr(ord(self.position[0]) + diagonal) + str(int(self.position[1]) + diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[1] = False
                else:
                    paths[1] = False
            if paths[2]:
                sq = chr(ord(self.position[0]) + diagonal) + str(int(self.position[1]) - diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[2] = False
                else:
                    paths[2] = False
            if paths[3]:
                sq = chr(ord(self.position[0]) - diagonal) + str(int(self.position[1]) - diagonal)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[3] = False
                else:
                    paths[3] = False

            diagonal += 1

        distance = 1
        paths = [True, True, True, True] # left, right, up, down

        while True in paths:
            if paths[0]:
                sq = chr(ord(self.position[0]) - distance) + self.position[1]
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[0] = False
                else:
                    paths[0] = False
            if paths[1]:
                sq = chr(ord(self.position[0]) + distance) + self.position[1]
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[1] = False
                else:
                    paths[1] = False
            if paths[2]:
                sq = self.position[0] + str(int(self.position[1]) + distance)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[2] = False
                else:
                    paths[2] = False
            if paths[3]:
                sq = self.position[0] + str(int(self.position[1]) - distance)
                if sq in occupied and (occupied[sq] == None or occupied[sq].colour != self.colour):
                    legal.append(sq)
                    if occupied[sq] != None:
                        paths[3] = False
                else:
                    paths[3] = False

            distance += 1

        return legal


class King(Piece):

    def __init__(self, colour, position):
        super(King, self).__init__(colour, position)
        self.has_moved = False # to keep track of castles
        if colour == 'White':
            self.image = 'w_king'
        else:
            self.image = 'b_king'
        self.around = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    self.around.append(chr(ord(self.position[0]) + i) + str(int(self.position[1]) + j))


    def legal_moves(self, piece_list, occupied):
        '''
        Returns a list of squares a piece can move to
        '''
        legal = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    dest = chr(ord(self.position[0]) + i) + str(int(self.position[1]) + j)
                    if dest in occupied and (occupied[dest] == None or occupied[dest].colour != self.colour):
                        square_attacked = False
                        for piece in piece_list:
                            if piece.colour != self.colour:
                                if str(type(piece)) == "<class 'pieces.King'>":
                                    if dest in piece.around:
                                        square_attacked = True
                                        break
                                elif str(type(piece)) == "<class 'pieces.Pawn'>":
                                    if dest in piece.possible_captures():
                                        square_attacked = True
                                        break
                                elif dest in piece.legal_moves(piece_list, occupied):
                                    square_attacked = True
                                    break
                        if not square_attacked:
                            legal.append(dest)

        legal += self.legal_castle(piece_list, occupied)

        next_checker = []
        for sq in legal:
            original = self.position
            self.position = sq
            occupied[original] = None
            new = occupied[sq]
            occupied[sq] = self
            if not self.in_check(piece_list, occupied):
                next_checker.append(sq)
            self.position = original
            occupied[original] = self
            occupied[sq] = new

        return next_checker


    def legal_castle(self, piece_list, occupied):
        legal = []
        if self.has_moved == False and self.in_check(piece_list, occupied) == False:
            if str(type(occupied['a' + self.position[1]])) == "<class 'pieces.Rook'>" and occupied['a' + self.position[1]].has_moved == False: # queenside
                valid = True # check the squares between the rook and king
                for col in ['d', 'c', 'b']:
                    if occupied[col + self.position[1]] != None:
                        valid = False
                        break
                    for piece in piece_list:
                        if piece.colour != self.colour and str(type(piece)) != "<class 'pieces.King'>" and col + self.position[1] in piece.attacking_squares(piece_list, occupied):
                            valid = False
                            break
                    if valid == False:
                        break
                if valid:
                    legal.append('c' + self.position[1])
            if str(type(occupied['h' + self.position[1]])) == "<class 'pieces.Rook'>" and occupied['h' + self.position[1]].has_moved == False and occupied['h' + self.position[1]].colour == self.colour: #kingside

                valid = True # check the squares between the rook and king
                for col in ['f', 'g']:
                    if occupied[col + self.position[1]] != None:
                        valid = False
                        break
                    for piece in piece_list:
                        if piece.colour != self.colour and str(type(piece)) != "<class 'pieces.King'>" and col + self.position[1] in piece.attacking_squares(piece_list, occupied):
                            valid = False
                            break
                    if valid == False:
                        break
                if valid:
                    legal.append('g' + self.position[1])

        return legal


    def update_squares_around(self):
        self.around = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    self.around.append(chr(ord(self.position[0]) + i) + str(int(self.position[1]) + j))


    def move(self, dest, piece_list, occupied):
        if occupied[dest] == None:
            move.play()
            if dest in self.legal_castle(piece_list, occupied):
                if dest[0] == 'c':
                    occupied['a' + dest[1]].castle(occupied)
                elif dest[0] == 'g':
                    occupied['h' + dest[1]].castle(occupied)
        else:
            capture.play()
            piece_list.remove(occupied[dest])
            occupied[dest] = self

        self.has_moved = True
        occupied[self.position] = None
        self.position = dest
        occupied[self.position] = self
        self.state = 'Down'
        self.update_squares_around()


    def in_check(self, piece_list, occupied):
        '''
        Returns whether the king is in check or not
        '''
        for piece in piece_list:
            if piece.colour != self.colour and str(type(piece)) != "<class 'pieces.King'>" and self.position in piece.attacking_squares(piece_list, occupied):
                return True
        return False


    def draw(self, screen, outline, piece_list, occupied, player):
        if player == 'White':
            squares = squares_white
        else: # if player == 'Black'
            squares = squares_black
        if self.in_check(piece_list, occupied):
            check_square = pygame.image.load("Images\checked.png")
            check_square = pygame.transform.scale(check_square, (96, 96)).convert_alpha()
            screen.blit(check_square, squares[self.position])
        if self.state == 'Down':
            screen.blit(piece_images[self.image], squares[self.position])
        elif self.state == 'Selected':
            screen.blit(piece_images[self.image], squares[self.position])
            screen.blit(outline, squares[self.position])
            for sq in self.legal_moves(piece_list, occupied):
                screen.blit(outline, squares[sq])
        elif self.state == 'Lifted':
            for sq in self.legal_moves(piece_list, occupied):
                screen.blit(outline, squares[sq])
            screen.blit(piece_images[self.image], self.cords)
