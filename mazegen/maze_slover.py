from .maze_generator import MazeGenerator


def maze_slover(maze: MazeGenerator) -> str:
    entry_pos = maze.entry_pos
    exit_pos = maze.exit_pos

    queue: list[tuple[int, int]] = [entry_pos]# dallanıcak listeyi tutuyor
    visited: set[tuple[int, int]] = {entry_pos}
    came_from: dict[tuple[int, int], tuple[tuple[int, int], str]] = {} # hangi cell e hangi cell den geldigimizi
    #exit bulundugunda tüm yolların bir önceki yolunu tutuyor
    while queue:

        current_cell = queue.pop(0)# işlem yaptıgımız hücreyi cıkarıyoruz
        curr_x, curr_y = current_cell
            
        if current_cell == exit_pos: # base case 
            break

        for dir, (x, y) in maze._DIRECTIONS.items(): # tüm yönlere geziyoruz
            new_x = curr_x + x
            new_y = curr_y + y

            if not 0 <= new_x < maze.width_x or not 0 <= new_y < maze.height_y:
                continue# yeni yön sınır dışı mı
            if is_wall(curr_x, curr_y, dir, maze):
                continue # yeni yönün duvarı kapalıysa geç
            if (new_x, new_y) in visited:
                continue # yeni yöne daha önce gidildiyse geç
            
            #duvarı açık gidilebilir yönü 
            visited.add((new_x, new_y))# listeye ekle
            queue.append((new_x, new_y))# kuyruğa ekle daha sonra onun komsularına bakılacak
            came_from[(new_x, new_y)] = ((curr_x, curr_y), dir) # ve o hücreye nerden geldigini tut

    path: list[str] = []
    cell = exit_pos
    while cell != entry_pos:
        if cell not in came_from:
            return "" # yol bulunamadı

        parent_cell, dir = came_from[cell]#exitten baslayarak cocuguna bak
        path.append(dir)#yönü tut
        cell = parent_cell# cocuga geç onun nerden geldigine bak
        # exitten entry e gidiş yolunu görüyosun

    path.reverse()
    return "".join(path)
 
#geçilebilir yönlerin listesini döndürür baba handmade   
def is_wall(x: int, y: int, dir: str,maze: MazeGenerator) -> bool:
        cell = maze.grid[y][x]

        if dir == "N":
            return cell.north
        if dir == "E":
            return cell.east
        if dir == "S":
            return cell.south
        if dir == "W":
            return cell.west
        raise ValueError(f"Unknown direction: '{dir}'")
