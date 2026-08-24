from collections.abc import Callable

from mazegen import MazeGenerator, maze_slover

ConfigDict = dict[str, int | str | bool | tuple[int, int]]

RESET = "\033[0m"

WALL_COLORS = [
    (235, 235, 238),  # white (default)
    (255, 215, 0),    # gold
    (100, 200, 255),  # sky blue
    (150, 255, 150),  # mint green
]
LOCKED_BG = (110, 113, 118)   # "42" pattern — always this gray, unaffected by rotation
ENTRY_BG = (176, 58, 199)     # purple
EXIT_BG = (214, 39, 42)       # red
PATH_BG = (60, 140, 220)      # solution-path highlight (only shown when toggled on)


def bg(rgb: tuple[int, int, int]) -> str:
    return f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"


def path_pixels(gen: MazeGenerator, path_str: str) -> set[tuple[int, int]]:
    x, y = gen.entry_pos
    px, py = 2 * x + 1, 2 * y + 1
    pixels = {(px, py)}
    for d in path_str:
        dx, dy = gen._DIRECTIONS[d]
        pixels.add((px + dx, py + dy))
        px, py = px + 2 * dx, py + 2 * dy
        pixels.add((px, py))
    return pixels


def build_pixel_grid(gen: MazeGenerator) -> list[list[str]]:
    w, h = 2 * gen.width_x + 1, 2 * gen.height_y + 1
    pixels = [["wall"] * w for _ in range(h)]

    for y in range(gen.height_y):
        for x in range(gen.width_x):
            cell = gen.grid[y][x]
            px, py = 2 * x + 1, 2 * y + 1
            if (x, y) == gen.entry_pos:
                pixels[py][px] = "entry"
            elif (x, y) == gen.exit_pos:
                pixels[py][px] = "exit"
            elif (x, y) in gen.locked_cells:
                pixels[py][px] = "locked"
            else:
                pixels[py][px] = "open"

            if not cell.east:
                pixels[py][px + 1] = "open"
            if not cell.south:
                pixels[py + 1][px] = "open"

    return pixels


def render_maze(
    gen: MazeGenerator,
    show_path: bool = False,
    wall_color_idx: int = 0,
) -> str:
    pixels = build_pixel_grid(gen)
    path = path_pixels(gen, maze_slover(gen)) if show_path else set()
    wall_bg = bg(WALL_COLORS[wall_color_idx])

    lines = []
    for py, row in enumerate(pixels):
        line = ""
        for px, kind in enumerate(row):
            if kind == "wall":
                line += wall_bg + "  " + RESET
            elif kind == "entry":
                line += bg(ENTRY_BG) + "  " + RESET
            elif kind == "exit":
                line += bg(EXIT_BG) + "  " + RESET
            elif kind == "locked":
                line += bg(LOCKED_BG) + "  " + RESET
            elif show_path and (px, py) in path:
                line += bg(PATH_BG) + "  " + RESET
            else:
                # colorless / transparent — no background code at all
                line += "  "
        lines.append(line)
    return "\n".join(lines)


def run_menu(
    build_maze: Callable[[ConfigDict], MazeGenerator],
    config: ConfigDict,
) -> None:
    gen = build_maze(config)
    show_path = False
    wall_idx = 0

    while True:
        print(render_maze(gen, show_path, wall_idx))
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colours")
        print("4. Quit")
        choice = input("Choice? (1-4): ").strip()

        if choice == "1":
            try:
                fresh_config = dict(config)
                fresh_config.pop("SEED", None)
                gen = build_maze(fresh_config)
            except ValueError as e:
                print(f"[ERROR] Could not regenerate: {e}")
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            wall_idx = (wall_idx + 1) % len(WALL_COLORS)
        elif choice == "4":
            break
        else:
            print("Invalid choice, try again.")