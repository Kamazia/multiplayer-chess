from tkinter import *
from shapes import Color, Empty

#from board import Board
from playing_area import ChessBoard


class VisualInterface:

    square_size = 50

    images = {}
    selected_figure = None
    possible_move = None

    first_color = 'sienna2'
    second_color = 'burlywood2'
    highlight_color = 'PaleGreen1'

    def __init__(self,root,chessboard) -> None:
        self.chessboard:ChessBoard = chessboard
        self.root:Tk = root

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

                if self.possible_move and [j,i] in self.possible_move:
                    self.canvas.create_rectangle(x1, y1, x2, y2,fill=self.highlight_color,tags="area")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2,fill=color,tags="area")
                color = self.first_color if color == self.second_color else self.second_color
        self.canvas.tag_raise("image")        
        self.canvas.tag_lower("area")

    def draw_figurines(self) -> None:
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
        print(selected_column,selected_row)
        x_y = self.chessboard.make_moves_two(selected_column,selected_row)

        self.possible_move = x_y

        self.draw_board()




if __name__ == "__main__":
    game_board = ChessBoard()
    root = Tk()

    gui = VisualInterface(root,game_board)
    gui.draw_board()
    gui.draw_figurines()

    root.mainloop()