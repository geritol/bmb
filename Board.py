from Board_settings import *


class Board:
    def __init__(self, state):
        self.state = state
        self.height = len(self.state['cells'])
        self.width = len(self.state['cells'][0])

    def __str__(self):
        """
        Returns the Board in a more human readable format
        :return: str representation of the Board
        """
        res = ''
        for i, line in enumerate(self.state['cells']):
            for j, cell in enumerate(line):
                value = self.helper_draw_cell(cell)
                if self.cell_has_enemy(i, j):
                    value = 'X'
                if self.cell_has_unit(i, j):
                    value = 'O'

                res += value
            res += "\n"
        return res

    def evaluate(self):
        """
        Calculates how good the current state is.
        :return: score of the current state
        """
        score = 0

        # +++ number off cells owned
        cell_count_owned = self.get_cell_count_owned_by(US)
        score += cell_count_owned * SCORE['cell-in-our-possession-multiplier']

        # ++ closeness to 'border'
        # TODO: implement search algo to closest cell that is not ours
        # Probably wont need this for now, as other factors will favorise
        # actions that lead to getting cells in our possession

        # -- tail collision
        for i, line in enumerate(self.state['cells']):
            for j, cell in enumerate(line):
                if self.is_cell_pending(cell) and self.cell_has_enemy(i, j):
                    score += SCORE['tail-collision']

        # --- head collision
        for unit in self.get_units():
            collision = self.cell_has_enemy(unit['position']['x'], unit['position']['y'])
            if collision:
                score += SCORE['head-collision']

        # --- our head collides with the tail
        # TODO!

        # ---- off board
        for unit in self.get_units():
            is_off = self.is_off_board(unit['position']['x'], unit['position']['y'])
            if is_off:
                score += SCORE['off-board']
                return score
        return score

    def is_cell_pending(self, cell):
        return 'unit' in cell['attack'] and cell['attack']['can']

    def get_cell_count_owned_by(self, player):
        cells_owned = 0
        for line in self.state['cells']:
            for cell in line:
                if cell['owner'] == player:
                    cells_owned += 1
        return cells_owned

    def is_off_board(self, x, y):
        if x < 0 or y < 0:
            return True
        if x > self.height -1 or y > self.width - 1:
            return True
        return False

    def helper_draw_cell(self, cell):
        if 'unit' in cell['attack']:
            return '-'
        if cell['owner'] == ENEMY:
            return '.'
        elif cell['owner'] == US:
            return ':'

    def get_enemies(self):
        return self.state['enemies']

    def get_units(self):
        return self.state['units']

    def get_cell(self, x, y):
        return self.state['cells'][y][x]

    def cell_has_enemy(self, x, y):
        res = False
        for enemy in self.get_enemies():
            res = enemy['position']['x'] == x and enemy['position']['y'] == y
        return res

    def cell_has_unit(self, x, y):
        res = False
        for unit in self.get_units():
            res = unit['position']['x'] == x and unit['position']['y'] == y
        return res
