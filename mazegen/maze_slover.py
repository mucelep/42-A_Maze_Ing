from .maze_generator import MazeGenerator


def maze_slover(maze: MazeGenerator) -> str:
    entry_pos = maze.entry_pos
    exit_pos = maze.exit_pos

    queue: list[tuple[int, int]] = [entry_pos]
    visited: set[tuple[int, int]] = {entry_pos}
    came_from: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
    
    while queue:
        
        current_cell = queue.pop(0)
        curr_x, curr_y = current_cell
            
        if current_cell == exit_pos:
            break

        for dir, (x, y) in maze._DIRECTIONS.items():
            new_x = curr_x + x
            new_y = curr_y + y
        
            if not 0 <= new_x < maze.width_x or not 0 <= new_y < maze.height_y:
                continue
            if is_wall(curr_x, curr_y, dir, maze):
                continue
            if (new_x, new_y) in visited:
                continue

            visited.add((new_x, new_y))
            queue.append((new_x, new_y))
            came_from[(new_x, new_y)] = ((curr_x, curr_y), dir)

    path: list[str] = []
    cell = exit_pos
    while cell != entry_pos:
        child_cell, dir = came_from[cell]
        path.append(dir)
        cell = child_cell

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
