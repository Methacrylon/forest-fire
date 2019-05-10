import sys
import src.engine.grid as gd

class TestGrid:

    def grid_is_empty(self, grid):
        return all([cell == gd.EMPTY for cell in grid])

    def test_constants(self):
        assert gd.EMPTY == 'empty'
        assert gd.TREE == 'tree'
        assert gd.BURNING == 'burning'

    def test_coordonates(self):
        grid = gd.Grid(4, 5)
        grid._grid = [["{}{}".format(i,j) for i in range(grid.width)] for j in range(grid.height)]
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == grid._grid[y][x]

    def test_empty_grid(self):
        grid = gd.Grid(4, 5)
        assert self.grid_is_empty(grid)

    def test_len_grid(self):
        grid = gd.Grid(4, 5)
        assert len(grid) == 4 * 5

    def test_update_grid_burning_spread(self):
        previous_grid = [['empty', 'empty', 'empty', 'empty', 'empty'],
                        ['empty', 'tree', 'empty', 'empty', 'empty'],
                        ['empty', 'empty', 'tree', 'tree', 'empty'],
                        ['empty', 'empty', 'burning', 'empty', 'empty']]

        updated_grid = [['empty', 'empty', 'empty', 'empty', 'empty'],
                        ['empty', 'tree', 'empty', 'empty', 'empty'],
                        ['empty', 'empty', 'burning', 'burning', 'empty'],
                        ['empty', 'empty', 'empty', 'empty', 'empty']]
        grid = gd.Grid(4, 5)
        for x in range(grid.width):
            for y in range(grid.height):
                grid[x, y] = previous_grid[y][x]
        grid.update()
        for x in range(grid.width):
            for y in range(grid.height):
                assert grid[x, y] == updated_grid[y][x]

    def test_update_all_trees(self):
        grid = gd.Grid(4, 5, 1)
        assert self.grid_is_empty(grid)
        grid.update()
        for cell in grid:
            assert cell == gd.TREE

    def test_update_some_trees(self):
        import random
        random.seed(0)
        grid = gd.Grid(4, 5, 0.5)
        assert self.grid_is_empty(grid)
        grid.update()
        cells = [cell for cell in grid]
        assert cells == ['empty', 'empty', 'tree', 'tree', 'empty', 'tree', 'empty', 'tree', 'tree', 'empty', 'empty', 'empty', 'tree', 'empty', 'empty', 'tree', 'empty', 'empty', 'empty', 'empty']

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
