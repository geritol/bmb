US = 1
ENEMY = 0

class Board:
    def __init__(self, state):
        self.state = state
        self.height = 100
        self.width = 80

    def __str__(self):
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
        score += cell_count_owned * 10

        # ++ closeness to 'border'
        # TODO: implement search algo to closest cell that is not ours

        # -- tail collision
        # TODO: keep track of our tail && get if some enemy is on it or not
        # tail:

        # --- head collision
        for unit in self.state['units']:
            collision = self.cell_has_enemy(unit['position']['x'], unit['position']['y'])
            if collision: score -= 500

        # ---- off board
        for unit in self.state['units']:
            is_off = self.is_off_board(unit['position']['x'], unit['position']['y'])
            if is_off:
                score -= 1000
                return score
        return score

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

    def cell_has_enemy(self, x, y):
        res = False
        for enemy in self.state['enemies']:
            res = enemy['position']['x'] == x and enemy['position']['y'] == y
        return res

    def cell_has_unit(self, x, y):
        res = False
        for unit in self.state['units']:
            res = unit['position']['x'] == x and unit['position']['y'] == y
        return res