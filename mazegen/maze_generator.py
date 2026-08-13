import random
from .cell import Cell


class MazeGenerator:
    _DIRECTIONS = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0),
        }

    def __init__(self, width: int, height: int, seed: int | None = None):
        self.width = width
        self.height = height
        self.seed = seed

        if seed is not None:
            random.seed(seed)

        self.create_grid = self._create_grid(self.width, self.height)   

    def _create_grid(self,width_x: int, height_y: int) -> list[list[Cell]]:
        grid = []#erişim için grid[Y][X] önce satır sonra stun
        
        for y in range(height_y):# DIŞ döngü: kaç satır olacağını belirler (y = satır numarası)
            row = []# yeni satır için boş liste aç
            
            for x in range(width_x): #her satırda width kadar eleman olustur
                cell = Cell()
                row.append(cell)# ve o satıra ekle
                
            grid.append(row)# sonra satırları grid de birlestir (satırlar listesi)

        return grid
