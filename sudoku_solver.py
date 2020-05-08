"""This module defines the sudoku puzzle class which represents and (hopefully) solves them.

    This class implements my method for solving these puzzles, which I call 'subtraction'.
    In short, each cell is thought of as a list of possible values and our goal is to narrow each list to one item.

    Author: Taylor VanCoevering, 2020
"""


class Puzzle:

    def __init__(self, height=9, width=9, min_val=1, max_val=9, subgrid_size=3):
        """Define the dimensions of this puzzle, if needed."""
        self.height = height
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.subgrid_size = subgrid_size

        self.grid = []
        self.clear()

    def clear(self):
        """Clear the existing grid by replacing all items."""
        self.grid = [list(range(self.min_val, self.max_val + 1)) for _ in range(self.height * self.width)]

    def set_cell(self, x, y, value):
        """Set the value of the cell at interpretted position x,y."""
        if value < self.min_val or value > self.max_val:
            raise TypeError(value)
        self.grid[self.get_index(x, y)] = [value]
        self.update(x, y)

    def update(self, x, y):
        """Update each cell affected by a change in the cell at x,y."""
        cell_value = self.grid[self.get_index(x, y)]
        if len(cell_value) == 1:

            # We track this 'known-value' and remove it from any of this cell's row, col, or subgrid neighbors.
            # When a neighbor is updated, it is necessary that they also proc an update.
            known_value = cell_value[0]
            print(f'known-value: {known_value} from ({x}, {y})')

            # Update the cell's row
            for row_x in (i for i in range(self.width) if i != x):
                print(row_x, y)
                row_cell = self.grid[self.get_index(row_x, y)]
                if known_value in row_cell:
                    print(f'--{known_value} found in: {row_cell}')
                    if len(row_cell) <= 1:
                        print("Can't remove from here!")
                        raise SystemExit
                    row_cell.remove(known_value)
                    self.update(row_x, y)

            # Update the cell's column
            for col_y in (i for i in range(self.height) if i != y):
                print(x, col_y)
                col_cell = self.grid[self.get_index(x, col_y)]
                if known_value in col_cell:
                    print(f'--{known_value} found in: {col_cell}')
                    if len(col_cell) <= 1:
                        print("Can't remove from here!")
                        raise SystemExit
                    col_cell.remove(known_value)
                    self.update(x, col_y)

            # Using // to specify a floor-division
            cell_sg_x = x // self.subgrid_size
            cell_sg_y = y // self.subgrid_size

            # Update the cell's subgrid
            for subgrid_x in (i for i in range(self.subgrid_size*cell_sg_x, self.subgrid_size*(cell_sg_x+1))):
                for subgrid_y in (j for j in range(self.subgrid_size*cell_sg_y, self.subgrid_size*(cell_sg_y+1))):
                    if subgrid_x == x and subgrid_y == y:
                        # Skip the cell that proc'd the update
                        continue
                    print(subgrid_x, subgrid_y)
                    subgrid_cell = self.grid[self.get_index(subgrid_x, subgrid_y)]
                    if known_value in subgrid_cell:
                        print(f'--{known_value} found in: {subgrid_cell}')
                        if len(subgrid_cell) <= 1:
                            print("Can't remove from here!")
                            raise SystemExit
                        subgrid_cell.remove(known_value)
                        self.update(subgrid_x, subgrid_y)

            print(f'finished with known-value: {known_value} from ({x}, {y})')

    def solve(self):
        """Attempt to solve the puzzle. This method will recurse if it proc's any cell changes."""
        had_impact = False

        # 'Necessity' Check: check for values who are the only choice in their row/col/sg
        for y in range(self.height):
            row_cells = [self.grid[self.get_index(x, y)] for x in range(self.width)]
            print(f'row-{y}: {row_cells}')
            for i in range(self.min_val, self.max_val+1):
                print(f'--checking for: {i}')
                instance = None
                for x in range(self.width):
                    r_cell = row_cells[x]
                    if i in r_cell:
                        if instance is not None or (len(r_cell) == 1):
                            print(f'----found another occurrence of {i} in {r_cell}; breaking...')
                            instance = None
                            break
                        else:
                            print(f'----found first occurrence of {i} in {r_cell}')
                            instance = x
                if instance is not None:
                    had_impact = True
                    self.set_cell(instance, y, i)

        for x in range(self.width):
            col_cells = [self.grid[self.get_index(x, y)] for y in range(self.height)]
            print(f'col-{x}: {col_cells}')
            for i in range(self.min_val, self.max_val+1):
                print(f'--checking for: {i}')
                instance = None
                for y in range(self.height):
                    c_cell = col_cells[y]
                    if i in c_cell:
                        if instance is not None or (len(c_cell) == 1):
                            print(f'----found another occurrence of {i} in {c_cell}; breaking...')
                            instance = None
                            break
                        else:
                            print(f'----found first occurrence of {i} in {c_cell}')
                            instance = y
                if instance is not None:
                    had_impact = True
                    self.set_cell(x, instance, i)

        # TO DO: implement the necessity check for each subgrid
        pass

        if had_impact:
            print('IMPACT!')
            self.print()
            self.solve()
        else:
            print('Solved as much as I could:')
            self.print()

    def get_index(self, x, y):
        """Return the list-index associated with a given x,y pair."""
        return y * self.width + x

    def print(self):
        """Pretty-print the current puzzle state."""
        for i in range(self.height):
            row_values = [str(cell).ljust(27, ' ') for cell in self.grid[i*self.width:(i+1)*self.width]]
            print('  '.join(row_values))

    def from_string(self, s):
        """Build puzzle state from an input string. The string should list the value of each cell, left-to-right,
        top-to-bottom where '.' denotes an unknown and a number denotes a known-value. Note: only use single-digits."""
        for y in range(self.height):
            row_str = s[y*self.width:(y+1)*self.width]
            x = 0
            for c in row_str:
                if c == '.':
                    pass
                else:
                    self.set_cell(x, y, int(c))
                x += 1


if __name__ == '__main__':
    # Solving this puzzle
    ex = '2.1.7.8..' \
         '.4.....3.' \
         '8..2....5' \
         '47..65.93' \
         '6.5.3....' \
         '.........' \
         '...34.6..' \
         '..47...1.' \
         '79..5...8'

    p = Puzzle()
    p.print()

    p.from_string(ex)
    p.print()

    # Initial 'certain-solution' with no guesses.
    p.solve()

    # At this point, our solution can't be certain about any further changes, so the user must make a guess.
    # This cell had only two values remaining (5 or 9), so we make a coin-flip.
    p.set_cell(0, 1, 5)
    p.solve()
