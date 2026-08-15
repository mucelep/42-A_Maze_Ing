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
        self.width_x = width
        self.height_y = height
        self.seed = seed

        if seed is not None:
            random.seed(seed)

        self.grid = self._create_grid()   

    def _create_grid(self) -> list[list[Cell]]:
        grid = []#erişim için grid[Y][X] önce satır sonra stun
        
        for y in range(self.height_y):# DIŞ döngü: kaç satır olacağını belirler (y = satır numarası)
            row = []# yeni satır için boş liste aç
            
            for x in range(self.width_x): #her satırda width kadar eleman olustur
                cell = Cell()
                row.append(cell)# ve o satıra ekle
                
            grid.append(row)# sonra satırları grid de birlestir (satırlar listesi)

        return grid

    def _generate_maze(self):
        start_x, start_y = 0, 0
        visited: set[tuple[int, int]] = set()#gezilen hücrelerelerin kordinatları
        stack:   list[tuple[int, int]]#islem yaptıgımız hücrelerin yolu
        
        visited.add((start_x, start_y))
        stack = [(start_x, start_y)]
        while stack:
            x, y = stack[-1]
            
            neighbors = self._get_unvisited_neighbors(x, y, visited)
            
            if neighbors:
                new_x, new_y, direction = random.choice(neighbors)
                self._remove_wall(x, y, new_x, new_y, direction)

                visited.add((new_x, new_y))
                stack.append((new_x, new_y))
            else:
                stack.pop()



    def _get_unvisited_neighbors(
        self, x: int, y: int, visited: set[tuple[int, int]]
        ) -> list[tuple[int, int, str]]:

        neighbors: list[tuple[int, int, str]] = []
        
        for direction, (dx, dy) in self._DIRECTIONS.items():#tüm yönleri gez
            new_x = x + dx
            new_y = y + dy
            
            if not (0 <= new_x < self.width_x and 0 <= new_y < self.height_y):
                continue
            
            if (new_x, new_y) in visited:
                continue
            
            neighbors.append((new_x, new_y, direction))
        
        return neighbors

    def _remove_wall(self, x: int, y: int, new_x: int, new_y: int, direction: str) -> None:
        current_cell: Cell = self.grid[y][x]
        neighbor_cell: Cell = self.grid[new_y][new_x]

        if direction == "N":
            current_cell.north = False
            neighbor_cell.south = False
        elif direction == "S":
            current_cell.south = False
            neighbor_cell.north = False
        elif direction == "E":
            current_cell.east = False
            neighbor_cell.west = False
        elif direction == "W":
            current_cell.west = False
            neighbor_cell.east = False