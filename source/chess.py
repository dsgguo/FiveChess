from pprint import pprint
from enum import Enum

class Player(Enum):
    BLACK = 1
    WHITE = 2

class Chess():
    def __init__(self):
        self.pos : str
        self.player : Player
        pass
        
    def drawbord(self):
        row = 6
        col = 6
        self.cheboard = [[0] * col for _ in range(row)]
        self.flash()
        pass
    
    def move(self, pos: str, player: Player):
        pos = pos.split(',')
        row = int(pos[0])
        col  = int(pos[1])
        self.cheboard[row][col] = player.value
        self._check_win(pos, player)
        self.flash()
        return self.cheboard, self._check_win(pos, player)
    
    def _check_win(self, pos, player):
        row = int(pos[0])
        col  = int(pos[1])
        # four directions for checking
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        n = len(self.cheboard) 
        for dx, dy in directions:
            count = 1  
            x, y = row + dx, col + dy
            while 0 <= x < n and 0 <= y < n and self.cheboard[x][y] == player.value:
                count += 1
                x += dx
                y += dy
            x, y = row - dx, col - dy
            while 0 <= x < n and 0 <= y < n and self.cheboard[x][y] == player.value:
                count += 1
                x -= dx
                y -= dy
            if count >= 5:
                print('winner:', player.name)
                return True
        return False
    
    def flash(self):
        pprint(self.cheboard)
        pass

