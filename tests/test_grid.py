import random
import src.engine.grid as gd

class TestGrid:

    def grid_is_empty(self, grid):
        return all([cell == gd.EMPTY for cell in grid])

    def test_constants(self):
        assert gd.EMPTY == 0
        assert gd.TREE == -1
        assert gd.BURNING == 5

    def test_coordinates(self):
        grid = gd.Grid(4, 5)
        grid._grid = [["{}{}".format(i,j) for i in range(grid.width)] for j in range(grid.height)]
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == grid._grid[y][x]

    def test_empty_grid(self):
        grid = gd.Grid(4, 5)
        assert self.grid_is_empty(grid)

    def test_initial_state(self):
        random.seed(0)
        initial_grid = [[-1, -1, -1, -1, -1],
                        [-1, -1, -1, 0, -1],
                        [-1, -1, -1, -1, -1],
                        [-1, -1, -1, -1, -1],
                        [-1, 0, 0, 0, 0],
                        [-1, -1, 0, -1, 0]]
        grid = gd.Grid(6, 5, planting_rate=0.3, initial_state=True)
        assert grid._grid == initial_grid

    def test_len_grid(self):
        grid = gd.Grid(4, 5)
        assert len(grid) == 4 * 5


    def test_burning_ash_cycle(self):
        start_grid = [[-1, 0, 5]]
        ash_1_grid = [[-1, 0, 4]]
        ash_2_grid = [[-1, 0, 3]]
        ash_3_grid = [[-1, 0, 2]]
        ash_4_grid = [[-1, 0, 1]]
        empty_grid = [[-1, 0, 0]]
        grid = gd.Grid(1, 3)

        for x in range(grid.width):
            for y in range(grid.height):
                grid[x, y] = start_grid[y][x]
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == ash_1_grid[y][x]
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == ash_2_grid[y][x]
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == ash_3_grid[y][x]
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == ash_4_grid[y][x]
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == empty_grid[y][x]

    def test_update_grid_burning_spread(self):
        previous_grid = [[0, 0, 0, 0, 0],
                        [0, -1, 0, 0, 0],
                        [0, 0, -1, -1, 0],
                        [0, 0, 5, 0, 0]]

        updated_grid_1 = [[0, 0, 0, 0, 0],
                         [0, -1, 0, 0, 0],
                         [0, 0, 5, 5, 0],
                         [0, 0, 4, 0, 0]]

        updated_grid_2 = [[0, 0, 0, 0, 0],
                         [0, 5, 0, 0, 0],
                         [0, 0, 4, 4, 0],
                         [0, 0, 3, 0, 0]]

        updated_grid_3 = [[0, 0, 0, 0, 0],
                         [0, 4, 0, 0, 0],
                         [0, 0, 3, 3, 0],
                         [0, 0, 2, 0, 0]]
        grid = gd.Grid(4, 5)
        for x in range(grid.width):
            for y in range(grid.height):
                grid[x, y] = previous_grid[y][x]
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == updated_grid_1[y][x]
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == updated_grid_2[y][x]
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == updated_grid_3[y][x]

    def test_update_all_trees(self):
        grid = gd.Grid(4, 5, 1)
        assert self.grid_is_empty(grid)
        grid.update()
        for cell in grid:
            assert cell == gd.TREE

    def test_update_some_trees(self):
        """
        Seed is hardcoded, so random is predictable and we can check some trees appeared.
        """
        random.seed(0)
        grid = gd.Grid(4, 5, 0.5)
        assert self.grid_is_empty(grid)
        grid.update()
        cells = [cell for cell in grid]
        assert cells == [0, 0, -1, -1, 0, -1, 0, -1, -1, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0]

    def test_update_lightning_on_empty(self):
        grid = gd.Grid(4, 5, 0, 1)
        assert self.grid_is_empty(grid)
        grid.update()
        assert self.grid_is_empty(grid)

    def test_update_lightning_on_tree(self):
        """
        Seed is hardcoded, so we can predict where the lightning will strike.
        """
        random.seed(0)
        grid = gd.Grid(4, 5, 0, 1)
        for x in range(grid.width):
            for y in range(grid.height):
                grid[x, y] = gd.TREE
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                if x == 3 and y == 0:
                    assert grid[x, y] == gd.BURNING
                else:
                    assert grid[x, y] == gd.TREE

    def test_update_lightning_rate(self):
        """
        Seed is hardcoded, so we can predict when and where the lightning will strike.
        """
        random.seed(0)
        grid = gd.Grid(4, 5, 0, 0.5)
        for x in range(grid.width):
            for y in range(grid.height):
                grid[x, y] = gd.TREE
        grid.update()
        for cell in grid:
            assert cell == gd.TREE
        grid.update()
        for cell in grid:
            assert cell == gd.TREE
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                if x == 2 and y == 3:
                    assert grid[x, y] == gd.BURNING
                else:
                    assert grid[x, y] == gd.TREE

    def test_get_neighbor_corner_0_0(self):
        grid = gd.Grid(4, 5)
        neighbor = [cell for cell in grid.get_neighbor(0, 0)]
        assert neighbor == [(0, 1), (1, 0), (1, 1)]

    def test_get_neighbor_corner_w_0(self):
        grid = gd.Grid(4, 5)
        neighbor = [cell for cell in grid.get_neighbor(grid.width - 1, 0)]
        assert neighbor == [(3, 0), (3, 1), (4, 1)]

    def test_get_neighbor_corner_w_h(self):
        grid = gd.Grid(4, 5)
        neighbor = [cell for cell in grid.get_neighbor(grid.width - 1, grid.height - 1)]
        assert neighbor == [(3, 2), (3, 3), (4, 2)]

    def test_get_neighbor_corner_0_h(self):
        grid = gd.Grid(4, 5)
        neighbor = [cell for cell in grid.get_neighbor(0, grid.height - 1)]
        assert neighbor == [(0, 2), (1, 2), (1, 3)]

    def test_get_neighbor_edge_vert(self):
        grid = gd.Grid(4, 5)
        neighbor = [cell for cell in grid.get_neighbor(0, 2)]
        assert neighbor == [(0, 1), (0, 3), (1, 1), (1, 2), (1, 3)]

    def test_get_neighbor_edge_horiz(self):
        grid = gd.Grid(4, 5)
        neighbor = [cell for cell in grid.get_neighbor(2, 0)]
        assert neighbor == [(1, 0), (1, 1), (2, 1), (3, 0), (3, 1)]

    def test_get_neighbor_center(self):
        grid = gd.Grid(4, 5)
        neighbor = [cell for cell in grid.get_neighbor(1, 2)]
        assert neighbor == [(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3)]
