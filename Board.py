class Board:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        for i, line in enumerate(self.state['cells']):
            for j, cell in enumerate(line):
                value = self.helper_draw_cell(cell)
                if self.has_enemy(j, i):
                    value = 'X'
                if self.has_unit(j, i):
                    value = 'O'

                print(value, end="")
            print()

    def helper_draw_cell(self, cell):
        if cell['owner'] == 0:
            return '.'
        elif cell['owner'] == 1:
            return ':'

    def has_enemy(self, x, y):
        res = False
        for enemy in self.state['enemies']:
            res = enemy['position']['x'] == x and enemy['position']['y'] == y
        return res

    def has_unit(self, x, y):
        res = False
        for unit in self.state['units']:
            res = unit['position']['x'] == x and unit['position']['y'] == y
        return res