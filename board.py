class Board:
    def __init__(self) -> None:
        self.board = [['x']*8 for _ in range(8)]

    def __repr__(self) -> str:
        result = ''

        for string in range(9):
            if string < 8:
                result += '  '.join(map(str,self.board[string])) +'  '+str(abs((string+1)- 9)) +'\n'
                pass
            else:
                result += '  '.join([chr(97+i) for i in range(8)]) +'  ' +'\n'

        return result.rstrip()
  
    def __getitem__(self,position):
        return self.board[position]

    def borders(self,x,y):
        if (x>=0 and x<8 and y>=0 and y<8):
            return True
        else:
            return False

if __name__ == '__main__':
    print(Board())