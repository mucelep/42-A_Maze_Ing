import random
from .cell import Cell


class MazeGenerator:
    _DIRECTIONS = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0),
        }

    def __init__(self,width: int, height: int,
                perfect: bool = True, seed: int | None = None):
        self.width_x = width
        self.height_y = height
        self.seed = seed

        if seed is not None:
            random.seed(seed)

        self.grid = self._create_grid()
        self.locked_cells = self._compute_42_pattern()

        if perfect:
            self._generate_maze()
        else:
            self._generate_maze()
            self._perfect_false()
           
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
            x, y = stack[-1]#current elemanı stack in en son elemanı yapıyoruz
            
            neighbors = self._get_unvisited_neighbors(x, y, visited)
            
            if neighbors:
                new_x, new_y, direction = random.choice(neighbors)
                self._remove_wall(x, y, new_x, new_y, direction)

                visited.add((new_x, new_y))
                stack.append((new_x, new_y))
            else:#komşu yoksa bir önceki elemana dönüyor
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
            
            if (new_x, new_y) in self.locked_cells:
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

    def _add_wall(self, x: int, y: int, new_x: int, new_y: int, direction: str) -> None:
            current_cell: Cell = self.grid[y][x]
            neighbor_cell: Cell = self.grid[new_y][new_x]

            if direction == "N":
                current_cell.north = True
                neighbor_cell.south = True
            elif direction == "S":
                current_cell.south = True
                neighbor_cell.north = True
            elif direction == "E":
                current_cell.east = True
                neighbor_cell.west = True
            elif direction == "W":
                current_cell.west = True
                neighbor_cell.east = True

    def _perfect_false(self):
        closed: list[tuple[int, int, int, int, str]] = self._get_closed_neighbors()
        count = max(2, int(len(closed) * 0.20))
        chosen = random.sample(closed, count)
        
        for x, y, new_x, new_y, direction in chosen:
            self._remove_wall(x, y, new_x, new_y, direction)

            if self._has_open_3x3():# eger 3x3 gap olustuysa geri ekle
                self._add_wall(x, y, new_x, new_y, direction)

        self._FBI_open_the_corner()
        self._open_42_corridor()

    def _get_closed_neighbors(self) -> list[tuple[int, int, int, int, str]]:

        closed : list[tuple[int, int, int, int, str]] = []

        for y in range(self.height_y):
            for x in range(self.width_x):
                cell = self.grid[y][x]

                if (x, y) in self.locked_cells:# kilitli ise gec 
                    continue
           
                if x + 1 < self.width_x and cell.east:# x sınır duvarı mı and dogusunda duvar var mı
                    if (x + 1, y) not in self.locked_cells: # duvarın karşı tarafı kilitli mi
                        closed.append((x, y, x + 1, y, "E"))

                if y + 1 < self.height_y and cell.south:
                    if (x, y + 1) not in self.locked_cells:
                        closed.append((x, y, x, y + 1, "S"))

        return closed

    def _FBI_open_the_corner(self):
        self._remove_wall(0, 0, 1, 0, "E")
        self._remove_wall(0, 0, 0, 1, "S")

        self._remove_wall(
            self.width_x -1, 0,
            self.width_x -2, 0, "W"
        )
        self._remove_wall(
            self.width_x - 1, 0,
            self.width_x - 1, 1, "S"
        )

        self._remove_wall(
            0, self.height_y - 1,
            0, self.height_y - 2, "N"
        )
        self._remove_wall(
            0, self.height_y - 1,
            1, self.height_y -1, "E"
        )

        self._remove_wall(
            self.width_x - 1, self.height_y -1,
            self.width_x - 2, self.height_y -1, "W"
        )

        self._remove_wall(
            self.width_x - 1, self.height_y -1,
            self.width_x - 1, self.height_y -2, "N"
        )

    def _compute_42_pattern(self) -> set[tuple[int, int]]:
        _DIGIT_4 = {
        (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4),
        }
        _DIGIT_2 = {
        (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4),
        }

        digit_width = 3 
        gap = 1
        pattern_width = digit_width * 2 + gap# patern boyutu
        pattern_height = 5 # uzunlugu
        center_x = self.width_x // 2
        center_y = self.height_y // 2
        start_x = center_x - pattern_width // 2
        start_y = center_y - pattern_height // 2

        locked_cells = set()
        for cx, cy in _DIGIT_4:
            real_x = start_x + cx # digit 4 ü gezip baslangıc kordinatına ekliyor
            real_y = start_y + cy
            locked_cells.add((real_x, real_y))# bunu listede tutuyor
        for cx, cy in _DIGIT_2:
            real_x = start_x + digit_width + gap + cx#a aynısını 2 için yapyıor 2 = baslangıc + 4 + gap + cx
            real_y = start_y + cy # gerek yok cunku yukarıdan assağı aynı 
            locked_cells.add((real_x, real_y))
        
        return locked_cells

    def _open_42_corridor(self):
        center_x = self.width_x // 2 # merkezi hesapliyor 10/2=5
        patern_height = 5
        start_y = (self.height_y - patern_height) // 2 # baslasngıc hesaplıyor 15-5 /2 = 5

        for y in range(start_y - 1, start_y + 5):
            self._remove_wall(center_x, y + 1, center_x, y, "N")

    def _has_open_3x3(self) -> bool:
        for start_y in range(self.height_y - 2):#  genislik 7 diyelim 3x kontrolü icin min
            for start_x in range(self.width_x - 2):

                # yatay bağlantılar
                all_open = True
                for row in range(start_y, start_y + 3):
                    for col in range(start_x, start_x + 2):
                        if self.grid[row][col].east:
                            all_open = False

                # dikey bağlantılar
                for row in range(start_y, start_y + 2):
                    for col in range(start_x, start_x + 3):
                        if self.grid[row][col].south:
                            all_open = False

                if all_open:
                    return True

        return False
