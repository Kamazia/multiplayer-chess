from tkinter import *
from shapes import Color, Empty

#from board import Board
from playing_area import ChessBoard


class VisualInterface:

    square_size = 50

    images = {}
    selected_figure = None
    possible_move = None

    first_color = 'tan2'
    second_color = 'burlywood1'
    highlight_color = 'DarkSeaGreen1'
    highlight_color_enemy = 'salmon'

    def __init__(self,root,chessboard) -> None:
        self.chessboard:ChessBoard = chessboard
        self.root:Tk = root

        self.root.geometry('420x420+1500+600')

        self.canvas = Canvas(
            master=self.root,
            width=self.square_size*8,
            height=self.square_size*8
        )
        self.canvas.pack(padx=8, pady=8)
        self.canvas.bind("<Button-1>", self.click_processing)

    def draw_board(self) -> None:
        color = self.second_color
        for i,row in enumerate(self.chessboard):
            color = self.first_color if color == self.second_color else self.second_color
            for j,col in enumerate(row):
                x1 = j * self.square_size
                y1 = i * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                if self.possible_move and ([j,i] in self.possible_move):
                    
                    enemy = [position for position in self.possible_move if not isinstance(self.chessboard[i][j],Empty)]
                    print('---',enemy)
                    if enemy:
                        self.canvas.create_rectangle(x1, y1, x2, y2,fill=self.highlight_color_enemy,tags="area")
                    else:
                        self.canvas.create_rectangle(x1, y1, x2, y2,fill=self.highlight_color,tags="area")

                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2,fill=color,tags="area")
                color = self.first_color if color == self.second_color else self.second_color
        self.canvas.tag_raise("image")
        self.canvas.tag_lower("area")

    def draw_figurines(self) -> None:
        self.canvas.delete('image')
        for i,row in enumerate(self.chessboard):
            for j,col in enumerate(row):
                if col.color == Color.black:
                    a = col.image[1]
                    if a not in self.images:
                        self.images[a] = PhotoImage(file=col.image[1])
                
                elif col.color == Color.white:
                    a = col.image[0]
                    if a not in self.images:
                        self.images[col.image[0]] = PhotoImage(file=col.image[0])

                else:
                    continue
                
                x0 = (j * self.square_size) + int(self.square_size / 2)
                y0 = (i * self.square_size) + int(self.square_size / 2)

                self.canvas.create_image(
                    x0,
                    y0,
                    image=self.images[a],
                    tags='image',
                )

    def click_processing(self,event):
        selected_column = int(event.x / self.square_size)
        selected_row = int(event.y / self.square_size)
        print("selected: ",selected_column,selected_row)

        if self.selected_figure:
            if [selected_column,selected_row] in self.possible_move:
                print('ходим на ',selected_column,selected_row)
                self.move(selected_column,selected_row)

                self.selected_figure = None
                self.possible_move = None

                selected_column = selected_row = None
                
                self.draw_figurines()


        self.focus(selected_column,selected_row)
        self.draw_board()

    def focus(self,selected_column,selected_row):
        if selected_column is None:
            return
        self.selected_figure = (selected_column,selected_row)
        self.possible_move = self.chessboard.make_moves_two(selected_column,selected_row)

    def move(self,x,y):
        print(f"откуда {self.selected_figure[0]} {self.selected_figure[1]} куда {x} {y}")
        self.chessboard[y][x] = self.chessboard[self.selected_figure[1]][self.selected_figure[0]]
        self.chessboard[self.selected_figure[1]][self.selected_figure[0]] = Empty()
        print(self.chessboard)



if __name__ == "__main__":
    game_board = ChessBoard()
    root = Tk()

    gui = VisualInterface(root,game_board)
    gui.draw_board()
    gui.draw_figurines()

    root.mainloop()