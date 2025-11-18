from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:

    """

    row = coord[0]
    col = coord[1] + 1
    new_grid = deepcopy(grid)
    new_grid[row][col] = " "
    return new_grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        direction = choice(["up", "right"])
        can_go_up = x > 1
        can_go_right = y < cols - 2

        if direction == "up":
            if can_go_up:
                grid[x - 1][y] = " "
            elif can_go_right:
                grid[x][y + 1] = " "
        elif direction == "right":
            if can_go_right:
                grid[x][y + 1] = " "
            elif can_go_up:
                grid[x - 1][y] = " "

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    result = []
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "X":
                result.append((x, y))
    return result


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    def find_zeroed(grid, index):
        res = []
        if index[0] != len(grid) - 1 and grid[index[0] + 1][index[1]] == 0:
            res.append((index[0] + 1, index[1]))
        if index[0] != 0 and grid[index[0] - 1][index[1]] == 0:
            res.append((index[0] - 1, index[1]))
        if index[1] != len(grid[0]) - 1 and grid[index[0]][index[1] + 1] == 0:
            res.append((index[0], index[1] + 1))
        if index[1] != 0 and grid[index[0]][index[1] - 1] == 0:
            res.append((index[0], index[1] - 1))

        return res

    ind = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == k:
                ind.append((x, y))
    for i in ind:
        zeroed = find_zeroed(grid, i)
        for j in zeroed:
            grid[j[0]][j[1]] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """

    def value_around_index(grid, index, value):
        results = []
        if index[0] != len(grid) - 1 and grid[index[0] + 1][index[1]] == value:
            results.append((index[0] + 1, index[1]))
        if index[0] != 0 and grid[index[0] - 1][index[1]] == value:
            results.append((index[0] - 1, index[1]))
        if index[1] != len(grid[0]) - 1 and grid[index[0]][index[1] + 1] == value:
            results.append((index[0], index[1] + 1))
        if index[1] != 0 and grid[index[0]][index[1] - 1] == value:
            results.append((index[0], index[1] - 1))

        return results

    path = []
    cur_value = int(grid[exit_coord[0]][exit_coord[1]])
    cur_coord = exit_coord
    path.append(exit_coord)
    while cur_value != 1:
        indices = value_around_index(grid, cur_coord, cur_value - 1)
        if not indices:
            grid[cur_coord[0]][cur_coord[1]] = " "
            path.pop()
            cur_coord = path[-1]
            cur_value = int(grid[cur_coord[0]][cur_coord[1]])
        else:
            path.append(indices[0])
            cur_coord = indices[0]
            cur_value = int(grid[cur_coord[0]][cur_coord[1]])
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    if coord[0] == len(grid) - 1 and coord[1] == len(grid[0]) - 1:
        return True
    elif coord[0] == 0 and coord[1] == 0:
        return True
    elif coord[0] == 0 and coord[1] == len(grid[0]) - 1:
        return True
    elif coord[0] == len(grid) - 1 and coord[1] == 0:
        return True

    if coord[0] == len(grid) - 1:
        if grid[coord[0] - 1][coord[1]] != " ":
            return True
    elif coord[0] == 0:
        if grid[coord[0] + 1][coord[1]] != " ":
            return True
    elif coord[1] == len(grid[0]) - 1:
        if grid[coord[0]][coord[1] - 1] != " ":
            return True
    elif coord[1] == 0:
        if grid[coord[0]][coord[1] + 1] != " ":
            return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) != 2:
        return grid, None

    for some_exit in exits:
        if encircled_exit(grid, some_exit):
            return grid, None

    start_coord, end_coord = exits

    q_grid = deepcopy(grid)
    for r, row in enumerate(q_grid):
        for c, cell in enumerate(row):
            if cell == " ":
                q_grid[r][c] = 0

    q_grid[start_coord[0]][start_coord[1]] = 0
    q_grid[end_coord[0]][end_coord[1]] = 0

    q_grid[start_coord[0]][start_coord[1]] = 1

    k = 1
    while q_grid[end_coord[0]][end_coord[1]] == 0:
        prev_q_grid = deepcopy(q_grid)
        make_step(q_grid, k)
        if q_grid == prev_q_grid:
            return grid, None
        k += 1

    path = shortest_path(q_grid, end_coord)

    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
