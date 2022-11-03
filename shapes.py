from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playing_field import Game


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
    def askew(self,board:Game,x,y,color,line) -> list:
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

    def check_line(self,board:Game,x,y,color,line) -> list:
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

    def __logic(self,board:Game,x,y,color:Color) -> (tuple[list, int] | None):
        if board.borders(x,y) and (board.get_color_field(x,y) == Color.empty or board.get_color_field(x,y) == color):
            return [x,y],board.get_color_field(x,y)


class Empty:
    def __init__(self) -> None:
        self.color = Color.empty

    def __repr__(self) -> str:
        return '.'

    def available_moves(self,board,x,y) -> list:
        return []


class Pawn(BasicFigure):
    icon = ('♙','♟︎')

    def available_moves(self,board:Game,x,y) -> list | None:
        if self.color == Color.white:
            return self.__white_logic(board,x,y)

        elif self.color == Color.black:
            return self.__black_logic(board,x,y)

    def __white_logic(self,board:Game,x,y) -> list | None:
            if board.borders(x,y) and board.get_color_field(x-1,y+1) == Color.black: # Рубит налево
                return [[x-1,y+1]]

            elif board.borders(x,y) and board.get_color_field(x-1,y+1) == Color.black: # Рубит направо
                return [[x+1,y+1]]

            elif board.borders(x,y) and board.get_color_field(x,y+1) == Color.empty: # Обычный ход
                return [[x,y+1]]

    def __black_logic(self,board:Game,x,y) -> list | None:
        if board.borders(x,y) and board.get_color_field(x-1,y-1) == Color.white: # Рубит налево
                return [[x-1,y-1]]

        elif board.borders(x,y) and board.get_color_field(x+1,y-1) == Color.white: # Рубит направо
            return [[x+1,y-1]]

        elif board.borders(x,y) and board.get_color_field(x,y-1) == Color.empty: # Обычный ход
            return [[x,y-1]]
         

class Horse(BasicFigure):
    icon = ('♘','♞')
    horse_ways = ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2))

    def available_moves(self,board:Game,x,y) -> list | None:
        moves = []

        for i in range(1,8):
            if self.color == Color.white and (match := self.__logic(board,x + self.horse_ways[i][1],y + self.horse_ways[i][0],Color.black)):
                moves.append(match)
            
            elif self.color == Color.black and (match := self.__logic(board,x + self.horse_ways[i][1],y + self.horse_ways[i][0],Color.white)):
                moves.append(match)
        
        return moves

    def __logic(self,board:Game,x,y,color:Color) -> list | None:
        if board.borders(x,y) and (board.get_color_field(x,y) == Color.empty or board.get_color_field(x,y) == color):
            return [x,y]


class Bishop(LongStroke):
    icon = ('♗','♝')
    
    def __check_line(self,board:Game,x,y,color,line) -> list:
        return super().askew(board,x,y,color,line)
     
    def available_moves(self,board:Game,x,y) -> list | None:
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

    def __check_line(self,board:Game,x,y,color,line) -> list:
        return super().check_line(board,x,y,color,line)

    def available_moves(self,board:Game,x,y) -> list | None:
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

    def __askew(self,board:Game,x,y,color,line) -> list:
        return super().askew(board,x,y,color,line)

    def __check_line(self,board:Game,x,y,color,line) -> list:
        return super().check_line(board,x,y,color,line)

    def available_moves(self,board:Game,x,y) -> list | None:
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


if __name__ == "__main__":
    print(Horse(Color.white) + Horse(Color.black) + '  Double Horse ' +  str(Horse(Color.black)) +' '+ str(Horse(Color.white)))