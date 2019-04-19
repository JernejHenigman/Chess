from Piece import *

class ChessBoard:
    def __init__(self, x_size, y_size):
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.blue = (51, 153, 255)
        self.green = (51, 255, 51)
        self.grey = (192, 192, 192)
        self.offset_x = 30
        self.offest_y = 30
        self.offset_piece = 10
        self.sqaure_size = 60
        self.is_check = False
        self.white_king_location = (0, 4)
        self.black_king_location = (7, 4)
        self.piece_that_gives_check_location = (-1, -1)
        self.piece_that_gives_pin_location = (-1, -1)
        self.block_check_location = (-1, -1)
        self.black_king_moved = False
        self.white_king_moved = False
        self.piece = None
        self.moves = []
        self.select_piece = True
        self.coords = (0, 0)
        self.current_color = "white"
        self.gameDisplay = pygame.display.set_mode((x_size, y_size))
        self.clock = pygame.time.Clock()
        self.gameExit = False

        self.white_pawn = ChessPiece("images/white_pawn.png", "white", "pawn")
        self.white_queen = ChessPiece("images/white_queen.png", "white", "queen")
        self.white_knight = ChessPiece("images/white_knight.png", "white", "knight")
        self.white_rook = ChessPiece("images/white_rook.png", "white", "rook")
        self.white_bishop = ChessPiece("images/white_bishop.png", "white", "bishop")
        self.white_king = ChessPiece("images/white_king.png", "white", "king")
        self.black_pawn = ChessPiece("images/black_pawn.png", "black", "pawn")
        self.black_queen = ChessPiece("images/black_queen.png", "black", "queen")
        self.black_rook = ChessPiece("images/black_rook.png", "black", "rook")
        self.black_bishop = ChessPiece("images/black_bishop.png", "black", "bishop")
        self.black_knight = ChessPiece("images/black_knight.png", "black", "knight")
        self.black_king = ChessPiece("images/black_king.png", "black", "king")
        self.chessBoard = self.init_chess_board()

        pygame.init()
        # background color
        self.gameDisplay.fill(self.red)
        # caption
        pygame.display.set_caption("ChessBoard")

    def init_chess_board(self):
        chessBoard = [[i for i in range(0, 8)] for j in range(0, 8)]
        chessBoard[1][0] = self.black_pawn
        chessBoard[1][1] = self.black_pawn
        chessBoard[1][2] = self.black_pawn
        chessBoard[1][3] = self.black_pawn
        chessBoard[1][4] = self.black_pawn
        chessBoard[1][5] = self.black_pawn
        chessBoard[1][6] = self.black_pawn
        chessBoard[1][7] = self.black_pawn
        chessBoard[0][0] = self.black_rook
        chessBoard[0][1] = self.black_knight
        chessBoard[0][2] = self.black_bishop
        chessBoard[0][3] = self.black_queen
        chessBoard[0][4] = self.black_king
        chessBoard[0][5] = self.black_bishop
        chessBoard[0][6] = self.black_knight
        chessBoard[0][7] = self.black_rook
        chessBoard[6][0] = self.white_pawn
        chessBoard[6][1] = self.white_pawn
        chessBoard[6][2] = self.white_pawn
        chessBoard[6][3] = self.white_pawn
        chessBoard[6][4] = self.white_pawn
        chessBoard[6][5] = self.white_pawn
        chessBoard[6][6] = self.white_pawn
        chessBoard[6][7] = self.white_pawn
        chessBoard[7][0] = self.white_rook
        chessBoard[7][1] = self.white_knight
        chessBoard[7][2] = self.white_bishop
        chessBoard[7][3] = self.white_queen
        chessBoard[7][4] = self.white_king
        chessBoard[7][5] = self.white_bishop
        chessBoard[7][6] = self.white_knight
        chessBoard[7][7] = self.white_rook

        return chessBoard

    def draw_chess_board(self):

        color = self.blue

        for i in range(0, 8):
            if (color == self.green):
                color = self.blue
            else:
                color = self.green
            for j in range(0, 8):
                pygame.draw.rect(self.gameDisplay, color,
                                 [self.offset_x + self.sqaure_size * j, self.offest_y + self.sqaure_size * i,
                                  self.sqaure_size, self.sqaure_size])
                if (type(self.chessBoard[i][j]) != int):
                    self.gameDisplay.blit(self.chessBoard[i][j].image,
                                          [self.offset_piece + self.offset_x + self.sqaure_size * j,
                                           self.offset_piece + self.offest_y + self.sqaure_size * i])

                if (color == self.green):
                    color = self.blue
                else:
                    color = self.green

                for move in self.moves:
                    if i == move[0] and j == move[1]:
                        pygame.draw.circle(self.gameDisplay, self.grey, [30 + self.offset_x + self.sqaure_size * j,
                                                                         30 + self.offest_y + self.sqaure_size * i], 10)

    def remove_piece(self, i, j):

        self.chessBoard[i][j] = -1

    def move_piece(self, i, j, piece):

        self.chessBoard[i][j] = piece

    def check_color(self, i, j):
        if self.chessBoard[i][j] == self.black_king or self.chessBoard[i][j] == self.black_queen or self.chessBoard[i][
            j] == self.black_pawn \
                or self.chessBoard[i][j] == self.black_knight or self.chessBoard[i][j] == self.black_rook or \
                self.chessBoard[i][j] == self.black_bishop:
            return "black"
        else:
            return "white"

    def get_piece(self, i, j):
        return self.chessBoard[i][j]

    def check_for_check(self, moves, color):
        king_loc = (-1, -1)
        if color == "black":
            king_loc = self.white_king_location
        else:
            king_loc = self.black_king_location
        for move in moves:
            if move[0] == king_loc[0] and move[1] == king_loc[1]:
                return True

        return False

    def find_locations_that_block_check(self, attacking_piece_location, king_location):
        locations = []

        # if check is deliverd by knight, we cannot block check
        if type(self.chessBoard[attacking_piece_location[0]][attacking_piece_location[1]]) == ChessPiece:
            if self.chessBoard[attacking_piece_location[0]][attacking_piece_location[1]].piece == "knight":
                return locations

        x = attacking_piece_location[0] - king_location[0]
        y = attacking_piece_location[1] - king_location[1]

        if x == 0 and y > 0:
            for k in range(1, abs(y)):
                locations.append((attacking_piece_location[0], attacking_piece_location[1] - k))
        elif x == 0 and y < 0:
            for k in range(1, abs(y)):
                locations.append((attacking_piece_location[0], attacking_piece_location[1] + k))
        elif x > 0 and y == 0:
            for k in range(1, abs(x)):
                locations.append((attacking_piece_location[0] - k, attacking_piece_location[1]))
        elif x < 0 and y == 0:
            for k in range(1, abs(x)):
                locations.append((attacking_piece_location[0] + k, attacking_piece_location[1]))
        elif x > 0 and y > 0:
            for k in range(1, abs(x)):
                locations.append((attacking_piece_location[0] - k, attacking_piece_location[1] - k))
        elif x < 0 and y > 0:
            for k in range(1, abs(x)):
                locations.append((attacking_piece_location[0] + k, attacking_piece_location[1] - k))
        elif y < 0 and x < 0:
            for k in range(1, abs(x)):
                locations.append((attacking_piece_location[0] + k, attacking_piece_location[1] + k))
        elif y < 0 and x > 0:
            for k in range(1, abs(x)):
                locations.append((attacking_piece_location[0] - k, attacking_piece_location[1] + k))

        return locations

    def pin(self, i, j, color, pieces, current_piece, king_location, sign):
        for k in range(1, 7):
            if self.check_if_opponent_piece(i + k * sign[0], j + k * sign[1], color):
                if i + k * sign[0] > 7: continue
                if j + k * sign[1] > 7: continue
                if i + k * sign[0] < 0: continue
                if j + k * sign[1] < 0: continue
                if self.chessBoard[i + k * sign[0]][j + k * sign[1]].piece == pieces[0] or \
                        self.chessBoard[i + k * sign[0]][j + k * sign[1]].piece == pieces[1]:
                    self.remove_piece(i, j)
                    possible_moves = self.possible_moves(i + k * sign[0], j + k * sign[1],
                                                         self.get_piece(i + k * sign[0], j + k * sign[1]))
                    self.move_piece(i, j, current_piece)
                    for move in possible_moves:
                        if move[0] == king_location[0] and move[1] == king_location[1]:
                            self.piece_that_gives_pin_location = (i + k * sign[0], j + k * sign[1])
                            return True
        return False

    # we check if piece is under pin
    def is_piece_pinned(self, i, j, color):
        king_location = (-1, -1)
        if color == "black":
            king_location = self.black_king_location
        else:
            king_location = self.white_king_location

        x = king_location[0] - i
        y = king_location[1] - j
        current_piece = self.chessBoard[i][j]

        if x == 0 and y > 0:
            pieces = ["rook", "queen"]
            sign = [0, -1]
            return self.pin(i, j, color, pieces, current_piece, king_location, sign)
        elif x == 0 and y < 0:
            pieces = ["rook", "queen"]
            sign = [0, 1]
            return self.pin(i, j, color, pieces, current_piece, king_location, sign)
        elif x > 0 and y == 0:
            pieces = ["rook", "queen"]
            sign = [-1, 0]
            return self.pin(i, j, color, pieces, current_piece, king_location, sign)
        elif x < 0 and y == 0:
            pieces = ["rook", "queen"]
            sign = [1, 0]
            return self.pin(i, j, color, pieces, current_piece, king_location, sign)
        elif x > 0 and y > 0:
            pieces = ["bishop", "queen"]
            sign = [-1, -1]
            return self.pin(i, j, color, pieces, current_piece, king_location, sign)
        elif x < 0 and y > 0:
            pieces = ["bishop", "queen"]
            sign = [1, -1]
            return self.pin(i, j, color, pieces, current_piece, king_location, sign)
        elif y < 0 and x < 0:
            pieces = ["bishop", "queen"]
            sign = [1, 1]
            return self.pin(i, j, color, pieces, current_piece, king_location, sign)
        elif y < 0 and x > 0:
            pieces = ["bishop", "queen"]
            sign = [-1, 1]
            return self.pin(i, j, color, pieces, current_piece, king_location, sign)
        else:
            return False

    def check_if_opponent_piece(self, i, j, my_color):
        if i > 7: i = 7
        if j > 7: j = 7
        if i < 0: i = 0
        if j < 0: j = 0
        if type(self.chessBoard[i][j]) != int and self.check_color(i, j) != my_color:
            return True
        else:
            return False

    def check_if_team_piece(self, i, j, my_color):
        if i > 7: i = 7
        if j > 7: j = 7
        if i < 0: i = 0
        if j < 0: j = 0
        if type(self.chessBoard[i][j]) != int and self.check_color(i, j) == my_color:
            return True
        else:
            return False

    def check_if_square_empty(self, i, j):
        if i > 7: i = 7
        if j > 7: j = 7
        if i < 0: i = 0
        if j < 0: j = 0
        if type(self.chessBoard[i][j]) == int:
            return True
        else:
            return False

    def move_bishop_rook_queen(self, i, j, color, sign, moves):
        directions = [True] * len(sign)

        for l in range(0, len(sign)):
            for k in range(1, 8):
                if i + k * sign[l][0] > 7: continue
                if i + k * sign[l][0] < 0: continue
                if j + k * sign[l][1] > 7: continue
                if j + k * sign[l][1] < 0: continue

                if (self.check_if_opponent_piece(i + k * sign[l][0], j + k * sign[l][1], color)):
                    moves.append((i + k * sign[l][0], j + k * sign[l][1]))
                    break

                if (self.check_if_square_empty(i + k * sign[l][0], j + k * sign[l][1]) and directions[l]):
                    moves.append((i + k * sign[l][0], j + k * sign[l][1]))
                else:
                    directions[l] = False
                    break

    def move_knight(self, i, j, color, sign, moves):

        for l in range(0, 8):
            if i + sign[l][0] > 7: continue
            if i + sign[l][0] < 0: continue
            if j + sign[l][1] > 7: continue
            if j + sign[l][1] < 0: continue
            if self.check_if_square_empty(i + sign[l][0], j + sign[l][1]) or self.check_if_opponent_piece(
                    i + sign[l][0], j + sign[l][1], color):
                moves.append((i + sign[l][0], j + sign[l][1]))

    def move_king(self, i, j, color, sign, moves):
        for l in range(0, 8):
            if i + sign[l][0] > 7: continue
            if i + sign[l][0] < 0: continue
            if j + sign[l][1] > 7: continue
            if j + sign[l][1] < 0: continue
            if self.check_if_square_empty(i + sign[l][0], j + sign[l][1]) or self.check_if_opponent_piece(
                    i + sign[l][0], j + sign[l][1], color):
                moves.append((i + sign[l][0], j + sign[l][1]))

    def move_pawn(self, i, j, color, moves):

        if color == "white":
            rank = 6
            sign = -1
        else:
            rank = 1
            sign = 1

        if i == rank and self.check_if_square_empty(i + 1 * sign, j) and self.check_if_square_empty(i + 2 * sign,
                                                                                                    j):
            moves.append((i + 1 * sign, j))
            moves.append((i + 2 * sign, j))
        if i == rank and self.check_if_square_empty(i + 1 * sign, j) and self.check_if_square_empty(i + 2 * sign,
                                                                                                    j) and self.check_if_opponent_piece(
            i + 1 * sign, j - 1 * sign, color):
            moves.append((i + 1 * sign, j))
            moves.append((i + 2 * sign, j))
            moves.append((i + 1 * sign, j - 1 * sign))
        if i == rank and self.check_if_square_empty(i + 1 * sign, j) and self.check_if_square_empty(i + 2 * sign,
                                                                                                    j) and self.check_if_opponent_piece(
            i + 1 * sign, j + 1 * sign, color):
            moves.append((i + 1 * sign, j))
            moves.append((i + 2 * sign, j))
            moves.append((i + 1 * sign, j + 1 * sign))
        if i == rank and self.check_if_square_empty(i + 1 * sign, j) and not self.check_if_square_empty(
                i + 2 * sign,
                j):
            moves.append((i + 1 * sign, j))
        if self.check_if_square_empty(i + 1 * sign, j):
            moves.append((i + 1 * sign, j))
        if self.check_if_opponent_piece(i + 1 * sign, j + 1 * sign, color):
            moves.append((i + 1 * sign, j + 1 * sign))
        if self.check_if_opponent_piece(i + 1 * sign, j - 1 * sign, color):
            moves.append((i + 1 * sign, j - 1 * sign))

    def possible_moves(self, i, j, piece):
        moves = []

        if piece == self.black_pawn:
            self.move_pawn(i, j, "black", moves)

        if piece == self.white_pawn:
            self.move_pawn(i, j, "white", moves)

        if piece == self.white_king:
            sign = [[1, 1], [0, 1], [1, 0], [0, -1], [-1, 0], [-1, 1], [1, -1], [-1, -1]]
            self.move_king(i, j, "white", sign, moves)
            self.white_king_location = (i, j)

        if piece == self.black_king:
            sign = [[1, 1], [0, 1], [1, 0], [0, -1], [-1, 0], [-1, 1], [1, -1], [-1, -1]]
            self.move_king(i, j, "black", sign, moves)
            self.black_king_location = (i, j)

        if piece == self.black_knight:
            sign = [[2, 1], [1, 2], [1, -2], [2, -1], [-1, 2], [-2, 1], [-2, -1], [-1, -2]]
            self.move_knight(i, j, "black", sign, moves)

        if piece == self.white_knight:
            sign = [[2, 1], [1, 2], [1, -2], [2, -1], [-1, 2], [-2, 1], [-2, -1], [-1, -2]]
            self.move_knight(i, j, "white", sign, moves)

        if piece == self.black_bishop:
            sign = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
            self.move_bishop_rook_queen(i, j, "black", sign, moves)

        if piece == self.white_bishop:
            sign = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
            self.move_bishop_rook_queen(i, j, "white", sign, moves)

        if piece == self.black_rook:
            sign = [[1, 0], [-1, 0], [0, -1], [0, 1]]
            self.move_bishop_rook_queen(i, j, "black", sign, moves)

        if piece == self.white_rook:
            sign = [[1, 0], [-1, 0], [0, -1], [0, 1]]
            self.move_bishop_rook_queen(i, j, "white", sign, moves)

        if piece == self.black_queen:
            sign = [[1, 1], [-1, 1], [1, -1], [-1, -1], [1, 0], [-1, 0], [0, -1], [0, 1]]
            self.move_bishop_rook_queen(i, j, "black", sign, moves)

        if piece == self.white_queen:
            sign = [[1, 1], [-1, 1], [1, -1], [-1, -1], [1, 0], [-1, 0], [0, -1], [0, 1]]
            self.move_bishop_rook_queen(i, j, "white", sign, moves)

        return moves


    def check_all_pieces_for_check(self, color):
        for i in range(0, 8):
            for j in range(0, 8):
                if (type(self.chessBoard[i][j]) == ChessPiece):
                    if self.chessBoard[i][j].color == color:
                        possible_moves = self.possible_moves(i, j, self.get_piece(i, j))
                        if self.check_for_check(possible_moves, color):
                            self.piece_that_gives_check_location = (i, j)
                            self.is_check = True
                            break

    def find_pawns_attacking_locations(self, color):
        attacking_locations = []

        if color == "white":
            sign = [[-1, -1], [-1, 1]]
        else:
            sign = [[1, -1], [1, 1]]
        for i in range(0, 8):
            for j in range(0, 8):
                if (type(self.chessBoard[i][j]) == ChessPiece):
                    if self.chessBoard[i][j].color == color:
                        if self.chessBoard[i][j].piece == "pawn":
                            attacking_locations.append((i + sign[0][0], j + sign[0][1]))
                            attacking_locations.append((i + sign[1][0], j + sign[1][1]))

        attacking_locations = [i for i in attacking_locations if i[0] > -1 and i[1] > -1 and i[0] < 8 and i[1] < 8]
        attacking_locations = list(dict.fromkeys(attacking_locations))

        return attacking_locations

    def generate_kings_moves(self, i, j, color):

        kings_move = self.possible_moves(i, j, self.chessBoard[i][j])

        if color == "black":
            new_color = "white"
        else:
            new_color = "black"

        pawn_moves = self.find_pawns_attacking_locations(new_color)

        other_moves = []

        for k in range(0, 8):
            for l in range(0, 8):
                if (type(self.chessBoard[k][l]) == ChessPiece):
                    if self.chessBoard[k][l].color == new_color:
                        if self.chessBoard[k][l].piece != "pawn":
                            other_moves.append(self.possible_moves(k, l, self.chessBoard[k][l]))

        other_moves = [item for sublist in other_moves for item in sublist]
        all_moves = other_moves + pawn_moves
        all_moves = list(dict.fromkeys(all_moves))

        for move in all_moves:
            if move in kings_move:
                kings_move.remove(move)

        # remove king
        temp_king = self.chessBoard[i][j]
        self.chessBoard[i][j] = -1

        # need to eliminate possibilty for king to move into direction where attacking piece that is giving check can also move
        # this happens when attacking with rook, bishop or queen, since king is blocking that move possibility, 1 possible king move
        # under check was always forbiden. Figured this our only when I played the game.
        moves_from_checking_piece = self.possible_moves(self.piece_that_gives_check_location[0],
                                                        self.piece_that_gives_check_location[1],
                                                        self.chessBoard[self.piece_that_gives_check_location[0]][
                                                            self.piece_that_gives_check_location[1]])
        for move in moves_from_checking_piece:
            if move in kings_move:
                kings_move.remove(move)

        # put king back on the board
        self.chessBoard[i][j] = temp_king

        return kings_move

    def is_piece_that_gives_ckeck_protected(self):

        if not self.is_check:
            return False

        if self.current_color == "white":
            color = "black"
        else:
            color = "white"

        possible_moves = []
        temp_piece = self.chessBoard[self.piece_that_gives_check_location[0]][self.piece_that_gives_check_location[1]]
        self.chessBoard[self.piece_that_gives_check_location[0]][self.piece_that_gives_check_location[1]] = -1

        for k in range(0, 8):
            for l in range(0, 8):
                if (type(self.chessBoard[k][l]) == ChessPiece):
                    if self.chessBoard[k][l].color == color:
                        possible_moves.append(self.possible_moves(k,l,self.get_piece(k,l)))


        possible_moves = [item for sublist in possible_moves for item in sublist]
        possible_moves = list(dict.fromkeys(possible_moves))

        self.move_piece(self.piece_that_gives_check_location[0],self.piece_that_gives_check_location[1],temp_piece)

        for move in possible_moves:
            if move[0] == self.piece_that_gives_check_location[0] and move[1] == self.piece_that_gives_check_location[1]:
                return True

        return False

    def find_moves_under_check(self, i, j, king_location):
        defending_moves = []
        blocking_moves = []
        king_moves = []
        remove_attacker_moves = []
        moves_under_check = []
        blocking_locations = self.find_locations_that_block_check(self.piece_that_gives_check_location, king_location)

        # find move that removes attacker of the king
        for move in self.moves:
            if move[0] == self.piece_that_gives_check_location[0] and move[1] == self.piece_that_gives_check_location[1]:
                remove_attacker_moves.append(move)

        # find moves that blocks check by moving defending piece into the blocking location
        for move in self.moves:
            for b_move in blocking_locations:
                if b_move[0] == move[0] and b_move[1] == move[1]:
                    blocking_moves.append(move)

        # find moves with moving king
        if (i, j) == king_location:

            defending_moves = self.generate_kings_moves(i, j, self.current_color)
        else:
            defending_moves = remove_attacker_moves + blocking_moves

        if len(defending_moves) == 0:
            moves_under_check = []
        else:
            moves_under_check = defending_moves
            #king cant take attacking piece, if attacking piece is protected
            if (self.is_piece_that_gives_ckeck_protected()):
                if self.piece_that_gives_check_location in defending_moves:
                    defending_moves.remove(self.piece_that_gives_check_location)

        if (self.is_piece_pinned(i, j, self.current_color)):
            moves_under_check = []

        return moves_under_check

    def promote_pawn(self,i,j):
        piece = self.get_piece(i,j)
        if type(piece) == ChessPiece:

            if piece.piece == "pawn":
                if (piece.color == self.current_color):

                    if self.current_color == "white" and i == 0:
                        self.chessBoard[i][j] = self.white_queen
                    elif self.current_color == "black" and i == 7:
                        self.chessBoard[i][j] = self.black_queen

    def is_checkmate(self, king_location):
        possible_moves = []
        for k in range(0, 8):
            for l in range(0, 8):
                if (type(self.chessBoard[k][l]) == ChessPiece):
                    if self.chessBoard[k][l].color == self.current_color:
                        possible_moves.append(self.find_moves_under_check(k, l, king_location))

        possible_moves = [item for sublist in possible_moves for item in sublist]

        if len(possible_moves) == 0:
            print("checkmate")
            return True
        else:

            return False

    def find_moves_under_pin(self, i, j):
        moves_under_pin = []
        current_piece = self.get_piece(i, j)
        for move in self.moves:
            # remove pinning piece, thats fine, player is allowed to do that
            if move[0] == self.piece_that_gives_pin_location[0] and move[1] == \
                    self.piece_that_gives_pin_location[1]:
                moves_under_pin.append((move[0], move[1]))
                continue

            # we remove moving piece from current position
            self.remove_piece(i, j)
            # we save taken opponent move by our piece, so that we can later restore its position
            temp_piece = self.get_piece(move[0], move[1])

            # we move our piece on that location
            self.move_piece(move[0], move[1], current_piece)
            moves_that_might_deliver_check = self.possible_moves(self.piece_that_gives_pin_location[0],
                                                                 self.piece_that_gives_pin_location[1],
                                                                 self.get_piece(
                                                                     self.piece_that_gives_pin_location[0],
                                                                     self.piece_that_gives_pin_location[1]))
            # we remove our piece from temporary location
            self.remove_piece(move[0], move[1])
            # we move temporary taken piece into its original position
            self.move_piece(move[0], move[1], temp_piece)

            if self.current_color == "black":
                color = "white"
            else:
                color = "black"

            if (not self.check_for_check(moves_that_might_deliver_check, color)):
                moves_under_pin.append((move[0], move[1]))

            # we move our piece into original position
            self.move_piece(i, j, current_piece)

        return moves_under_pin

    # TODO
    def rook_can_see_king(self):
        return False

    # TODO
    def castling_squares_under_attack(self):
        return False

    # TODO
    def castling(self):
        if self.current_color == "white" and self.white_king_moved and not self.rook_can_see_king() and not self.castling_squares_under_attack():
            return "cannot castle white king"

        if self.current_color == "black" and self.black_king_moved and not self.rook_can_see_king() and not self.castling_squares_under_attack():
            return "cannot castle black king"

    # TODO
    def en_passant(self):
        pass

    def game(self, i, j):

        if self.select_piece:

            if (type(self.get_piece(i, j)) != ChessPiece):
                return "Invalid move"

            piece_color = self.check_color(i, j)

            if (piece_color != self.current_color):
                return "Invalid move"

            self.piece = self.get_piece(i, j)
            self.coords = (i, j)
            self.moves = self.possible_moves(i, j, self.piece)
            self.select_piece = False

            if self.piece.piece == "king":
                self.moves = self.generate_kings_moves(i, j, self.current_color)

            # check for pins, accordingly reduces move possibilities
            if (self.is_piece_pinned(i, j, self.current_color) and not self.is_check):
                self.moves = self.find_moves_under_pin(i, j)

            king_location = (-1, -1)
            if self.current_color == "black":
                king_location = self.black_king_location
            else:
                king_location = self.white_king_location

            if (self.is_check):
                self.moves = self.find_moves_under_check(i, j, king_location)

        else:

            player_move = (i, j)
            if player_move not in self.moves:
                self.moves = []
                self.select_piece = True
                return "Invalid move"
            self.remove_piece(self.coords[0], self.coords[1])
            self.move_piece(i, j, self.piece)
            self.is_check = False
            self.select_piece = True
            self.moves = []

            self.promote_pawn(i,j)

            # after player makes a move, we check if player deliverd a check to opponents king, we need for discovery checks
            self.check_all_pieces_for_check(self.current_color)

            if self.current_color == "white":
                self.current_color = "black"
                king_location = self.black_king_location
            else:
                self.current_color = "white"
                king_location = self.white_king_location

            if self.is_check:
                if self.is_checkmate(king_location):
                    self.moves = []

                    self.select_piece = False

    def run_game(self):
        while not self.gameExit:
            mx, my = pygame.mouse.get_pos()
            mj, mi = (int((mx - self.offset_x) / self.sqaure_size), int((my - self.offest_y) / self.sqaure_size))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameExit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(self.game(mi, mj))

            self.draw_chess_board()

            pygame.display.update()


chessBoard = ChessBoard(800, 600)
chessBoard.run_game()
