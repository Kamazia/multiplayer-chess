from __future__ import annotations
from dataclasses import dataclass
from tkinter import Button, Canvas, Tk
from typing import TYPE_CHECKING
from os import path



if TYPE_CHECKING:
    from playing_area import ChessBoard

BASE_PATH_IMG = path.dirname(path.abspath(__file__)) + "\\image\\"

@dataclass
class Color:
    white:int = 0
    black:int = 1
    empty:int = 2


class BasicFigure:
    def __init__(self,color) -> None:
        self.color = color

    def __repr__(self) -> str:
        return self.icon[self.color]
    
    def __add__(self,arg) -> str | None:
        if isinstance(arg,str):
            return f'{self}{arg}'

        elif isinstance(arg,int):
            return f'{self} {str(arg)}'

        elif isinstance(arg,BasicFigure):
            return f'{self} {arg}'


class LongStroke(BasicFigure):
    def askew(self,board:ChessBoard,x,y,color,line) -> list:
        moves_on_line = []
        for i in range(1,8):

            if line == 0:
                match = self.__logic(board,x+i,y+i,color)

            elif line == 1:
                match = self.__logic(board,x-i,y-i,color)

            elif line == 2:
                match = self.__logic(board,x-i,y+i,color)

            elif line == 3:
                match = self.__logic(board,x+i,y-i,color)

            if match:
                moves_on_line.append(match[0])
                if match[1] == color:
                    break
            else:
                break

        return moves_on_line

    def check_line(self,board:ChessBoard,x,y,color,line) -> list:
        moves_on_line = []
        for i in range(1,8):

            if line == 0:
                match = self.__logic(board,x+i,y,color)

            elif line == 1:
                match = self.__logic(board,x-i,y,color)

            elif line == 2:
                match = self.__logic(board,x,y+i,color)

            elif line == 3:
                match = self.__logic(board,x,y-i,color)

            if match:
                moves_on_line.append(match[0])
                if match[1] == color:
                    break
            else:
                break

        return moves_on_line

    def __logic(self,board:ChessBoard,x,y,color:Color) -> (tuple[list, int] | None):
        if board.borders(x,y) and (board.get_color_field(x,y) == Color.empty or board.get_color_field(x,y) == color):
            return [x,y],board.get_color_field(x,y)


class Empty:
    image = (BASE_PATH_IMG + "wE.png",BASE_PATH_IMG + "bE.png")

    def __init__(self) -> None:
        self.color = Color.empty

    def __repr__(self) -> str:
        return '.'

    def available_moves(self,board:ChessBoard,x,y) -> list:
        return []


class Pawn(BasicFigure):
    icon = ('♙','♟︎')
    image = (BASE_PATH_IMG + "wP.png",BASE_PATH_IMG + "bP.png")

    def available_moves(self,board:ChessBoard,x,y) -> list | None:
        if self.color == Color.white:
            return self.__white_logic(board,x,y)

        elif self.color == Color.black:
            return self.__black_logic(board,x,y)

    def __white_logic(self,board:ChessBoard,x,y) -> list | None:
            if board.borders(x,y) and board.get_color_field(x-1,y+1) == Color.black: # Рубит налево
                return [[x-1,y+1]]

            elif board.borders(x,y) and board.get_color_field(x+1,y+1) == Color.black: # Рубит направо
                return [[x+1,y+1]]

            elif board.borders(x,y) and board.get_color_field(x,y+1) == Color.empty: # Обычный ход
                if y == 1 and board.get_color_field(x,y+2) == Color.empty:
                    return [[x,y+1],[x,y+2]]
                return [[x,y+1]]

    def __black_logic(self,board:ChessBoard,x,y) -> list | None:
        if board.borders(x,y) and board.get_color_field(x-1,y-1) == Color.white: # Рубит налево
                return [[x-1,y-1]]

        elif board.borders(x,y) and board.get_color_field(x+1,y-1) == Color.white: # Рубит направо
            return [[x+1,y-1]]

        elif board.borders(x,y) and board.get_color_field(x,y-1) == Color.empty: # Обычный ход
            if y == 6 and board.get_color_field(x,y-2) == Color.empty:
                return [[x,y-1],[x,y-2]]
            return [[x,y-1]]
         

class Knight(BasicFigure):
    icon = ('♘','♞')
    image = (BASE_PATH_IMG + "wN.png",BASE_PATH_IMG + "bN.png")
    possible_move = ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2))

    def available_moves(self,board:ChessBoard,x,y) -> list | None:
        moves = []

        for i in range(0,8):
            if self.color == Color.white and (match := self.__logic(board,x + self.possible_move[i][1],y + self.possible_move[i][0],Color.black)):
                moves.append(match)
            
            elif self.color == Color.black and (match := self.__logic(board,x + self.possible_move[i][1],y + self.possible_move[i][0],Color.white)):
                moves.append(match)
        
        return moves

    def __logic(self,board:ChessBoard,x,y,color:Color) -> list | None:
        if board.borders(x,y) and (board.get_color_field(x,y) == Color.empty or board.get_color_field(x,y) == color):
            return [x,y]


class Bishop(LongStroke):
    icon = ('♗','♝')
    image = (BASE_PATH_IMG + "wB.png",BASE_PATH_IMG + "bB.png")

    def __check_line(self,board:ChessBoard,x,y,color,line) -> list:
        return super().askew(board,x,y,color,line)
     
    def available_moves(self,board:ChessBoard,x,y) -> list | None:
        moves = []

        for i in range(4):
            if self.color == Color.white:
                print(self.__check_line(board,x,y,Color.black,i))
                moves += self.__check_line(board,x,y,Color.black,i)

            elif self.color == Color.black:         
                print(self.__check_line(board,x,y,Color.white,i))
                moves += self.__check_line(board,x,y,Color.white,i)

        return moves


class Rook(LongStroke):
    icon = ('♖','♜')
    image = (BASE_PATH_IMG + "wR.png",BASE_PATH_IMG + "bR.png")

    def __check_line(self,board:ChessBoard,x,y,color,line) -> list:
        return super().check_line(board,x,y,color,line)

    def available_moves(self,board:ChessBoard,x,y) -> list | None:
        moves = []

        for i in range(4):
            if self.color == Color.white:
                print(self.__check_line(board,x,y,Color.black,i))
                moves += self.__check_line(board,x,y,Color.black,i)

            elif self.color == Color.black:         
                print(self.__check_line(board,x,y,Color.white,i))
                moves += self.__check_line(board,x,y,Color.white,i)

        return moves


class Queen(LongStroke):
    icon = ('♕','♛')
    image = (BASE_PATH_IMG + "wQ.png",BASE_PATH_IMG + "bQ.png")

    def __askew(self,board:ChessBoard,x,y,color,line) -> list:
        return super().askew(board,x,y,color,line)

    def __check_line(self,board:ChessBoard,x,y,color,line) -> list:
        return super().check_line(board,x,y,color,line)

    def available_moves(self,board:ChessBoard,x,y) -> list | None:
        moves = []

        for i in range(4):
            if self.color == Color.white:
                print(self.__check_line(board,x,y,Color.black,i))
                moves += self.__check_line(board,x,y,Color.black,i)
                moves += self.__askew(board,x,y,Color.black,i)

            elif self.color == Color.black:         
                print(self.__check_line(board,x,y,Color.white,i))
                moves += self.__check_line(board,x,y,Color.white,i)
                moves += self.__askew(board,x,y,Color.white,i)

        return moves


class King(BasicFigure):
    icon = ('♔','♚')
    image = (BASE_PATH_IMG + "wK.png",BASE_PATH_IMG + "bK.png")
    possible_move = ((0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1))
    
    def available_moves(self,board:ChessBoard,x,y) -> list | None:
        moves = []

        for i in range(0,8):
            if self.color == Color.white and (match := self.__logic(board,x + self.possible_move[i][1],y + self.possible_move[i][0],Color.black)):
                moves.append(match)
            
            elif self.color == Color.black and (match := self.__logic(board,x + self.possible_move[i][1],y + self.possible_move[i][0],Color.white)):
                moves.append(match)
        
        return moves

    def __logic(self,board:ChessBoard,x,y,color:Color) -> list | None:
        if board.borders(x,y) and (board.get_color_field(x,y) == Color.empty or board.get_color_field(x,y) == color):
            return [x,y]

if __name__ == "__main__":
    print(Knight(Color.white) + Knight(Color.black) + '  Double Horse ' +  str(Knight(Color.black)) +' '+ str(Knight(Color.white)))
