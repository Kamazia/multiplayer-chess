from board import Board
from shapes import Bishop, Color, Empty, Knight, King, Pawn, Queen, Rook


class ChessBoard(Board):
    def __init__(self) -> None:
        super().__init__()
        self.board = self.__start_position()

    def __repr__(self) -> str:
        return super().__repr__()

    def __switch_color(self,line) -> Color:
        if line == Color.white:
            return Color.white
        else:
            return Color.black

    def __start_position(self) -> Board:

        self.board = [[Empty()]*8 for _ in range(8)]

        for line in range(0,6+1,5):
            for position in range(8):
                self.board[line+1][position] = Pawn(self.__switch_color(line))
                
        for line in range(0,7+1,7):
            for position in range(1,6+1,5):
                self.board[line][position] = Knight(self.__switch_color(line))

        for line in range(0,7+1,7):
            for position in range(2,5+1,3):
                self.board[line][position] = Bishop(self.__switch_color(line))

        for line in range(0,7+1,7):
            for position in range(0,7+1,7):
                self.board[line][position] = Rook(self.__switch_color(line))

        for line in range(0,7+1,7):
            for position in range(3,4+1,1):
                self.board[line][position] = Queen(self.__switch_color(line))

        for line in range(0,7+1,7):
            for position in range(4,4+1,1):
                self.board[line][position] = King(self.__switch_color(line))


        return self.board

    def get_color_field(self,x,y):
        if (x<0 or x>7 or y<0 or y>7):
            return []
        return self.board[y][x].color

    def make_moves(self,x_from,y_from,x_to,y_to):
        #print(self.board[y_from][x_from])
        motion = self.board[y_from][x_from].available_moves(self,x_from,y_from)
        print(f'{self.board[y_from][x_from]} to {motion}')
        if [x_to,y_to] in motion:
            self.board[y_to][x_to] = self.board[y_from][x_from]
            self.board[y_from][x_from] = Empty()
            return self

    def make_moves_two(self,x_from,y_from):
        #print(self.board[y_from][x_from])
        motion = self.board[y_from][x_from].available_moves(self,x_from,y_from)
        print(f'{self.board[y_from][x_from]} to {motion}')
        return motion



if __name__ == '__main__':
    a = ChessBoard()


    '''a.make_moves(0,1,0,2)
    a.make_moves(0,2,0,3)
    a.make_moves(0,0,0,2)
    a.make_moves(0,2,4,2)
    a.make_moves(4,2,4,6)
    a.make_moves(4,6,1,6)
    a.make_moves(4,6,3,6)

    a.make_moves(0,6,0,5)
    a.make_moves(0,5,0,4)
    a.make_moves(0,7,0,5)
    a.make_moves(0,5,4,1)
    a.make_moves(3,5,3,6)

    a.make_moves(5,7,2,4)
    a.make_moves(2,4,6,0)

    a.make_moves(4,1,4,2)
    a.make_moves(5,0,0,5)

    a.make_moves(6,7,7,5)
    a.make_moves(1,0,0,2)
    a.make_moves(6,0,4,1)
    a.make_moves(1,7,2,5)

    a.make_moves(0,5,1,4)

    a.make_moves(3,7,6,4)
    a.make_moves(6,4,4,2)

    a.make_moves(3,0,4,2)

    a.make_moves(4,7,5,6)
    a.make_moves(4,7,4,6)
    a.make_moves(4,6,3,5)'''

    print(str(a)+'\n\n')