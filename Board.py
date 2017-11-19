from Board_settings import *


class Board:
    def __init__(self, state):
        self.state = state
        self.height = len(self.state['cells'])
        self.width = len(self.state['cells'][0])
        self.dead_by = {}

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
        deaths = self.dead_by

        if not deaths:
            deaths = self.calculate_deaths()

        for death_type, death_count in deaths.items():
            score += SCORE[death_type] * death_count

        return score

    def some_of_our_guys_die(self):
        if not self.dead_by:
            self.calculate_deaths()

        for death_type, death_count in self.dead_by.items():
            if death_count > 0:
                return True

        return False

    def calculate_deaths(self):
        res = {}

        # ---- off board
        res['off-board'] = 0
        for unit in self.get_units():
            is_off = self.is_off_board(unit['position']['x'], unit['position']['y'])
            if is_off:
                res['off-board'] += 1
                self.dead_by = res
                return res

        # -- tail collision
        res['tail-collision'] = 0
        for i, line in enumerate(self.state['cells']):
            for j, cell in enumerate(line):
                if self.is_cell_pending(cell) and self.cell_has_enemy(i, j):
                    res['tail-collision'] += 1

        # --- head collision
        res['head-collision'] = 0
        for unit in self.get_units():
            collision = self.cell_has_enemy(unit['position']['x'], unit['position']['y'])
            if collision:
                res['head-collision'] += 1

        # --- our head collides with the tail
        # res['head-tail-collision'] = 0
        # for unit in self.get_units():
        #     collision = self.cell_has_tail(unit['position']['y'], unit['position']['x'])
        #     if collision:
        #         res['head-tail-collision'] += 1

        self.dead_by = res
        return res

    # check if a cell is ours and cannot be attacked
    def is_cell_safe(self, x, y):
        cell = self.get_cell(x, y)
        return 'owner' in cell and cell['owner'] == US

    def is_cell_tail_of_unit(self, cell, unit_index):
        return 'unit' in cell['attack'] and cell['attack']['unit'] == unit_index  and 'can' in cell['attack'] and cell['attack']['can']

    def is_cell_pending(self, cell):
        return 'unit' in cell['attack'] and 'can' in cell['attack'] and cell['attack']['can']

    def can_enemy_attack_coordinates(self, x, y):
        cell = self.get_cell(x, y)
        return cell['attack'] and 'can' in cell['attack'] and cell['attack']['can']

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

    def get_cells(self):
        return [item for sublist in self.state['cells'] for item in sublist]

    def get_cell(self, x, y):
        return self.state['cells'][x][y]

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

    def cell_has_tail(self, y, x):
        cell = self.get_cell(x, y)
        return 'unit' in cell['attack'] and cell['attack']['unit'] == US and cell['attack']['can']

