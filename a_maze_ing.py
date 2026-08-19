from mazegen import MazeGenerator


def print_maze_ascii(gen: MazeGenerator) -> None:
    """Labirenti terminale basar - '42' desenindeki kilitli hücreleri '#' ile,
    normal koridorları boşluk ile gösterir.
    """
    width, height = gen.width_x, gen.height_y

    print("+" + "---+" * width)

    for y in range(height):
        # hücre içi + doğu duvarları
        line = "|"
        for x in range(width):
            cell = gen.grid[y][x]
            line += "###" if (x, y) in gen.locked_cells else "   "
            line += "|" if cell.east else " "
        print(line)

        # güney duvarları
        line = "+"
        for x in range(width):
            cell = gen.grid[y][x]
            line += "---" if cell.south else "   "
            line += "+"
        print(line)


if __name__ == "__main__":
    gen = MazeGenerator(width=15, height=9, perfect=True)
    print("=== PERFECT=True (15x9, seed=1) ===\n")
    print_maze_ascii(gen)

    print("\n\n=== PERFECT=False (15x9, seed=1) ===\n")
    gen2 = MazeGenerator(width=15, height=11, perfect=False)
    print_maze_ascii(gen2)


# # #!/usr/bin/env python3
# # from process_config import read_config_file
# # from process_config import validate_config
# # from mazegen import MazeGenerator


# # def main() -> None:
# #     try:
# #         config = read_config_file()
# #         validate_config(config)
# #     except ValueError as e:
# #         print(f"[ERROR] - {e}")
# #     maze = MazeGenerator(
# #         config["WIDTH"],
# #         config["HEIGHT"],
# #         config["ENTRY"],
# #         config["EXIT"],
# #         config["PERFECT"],
# #         config["SEED"]
# #     )
    
# # if __name__ == "__main__":
# #     main()