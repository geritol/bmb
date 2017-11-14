import copy

to_delta = {
    'left': -1,
    'right': +1,
    'up': -1,
    'down': +1
}

flip = {
    'left': 'right',
    'right': 'left',
    'up': 'down',
    'down': 'up'
}

class Game:
    def __init__(self, starting_Board):
        self.starting_Board = starting_Board
        self.current_Board = starting_Board

    def move(self, action_list):
        """
        Applies the actions to self.current_Board, and returns the new Board
        """
        next_board = copy.deepcopy(self.current_Board)

        # move units
        next_units = []
        for action in action_list:
            next_unit = copy.deepcopy(next_board.get_units()[action['unit']])
            next_unit['direction'] = action['direction']
            if action['direction'] in ['up', 'down']:
                next_unit['position']['x'] += to_delta[action['direction']]
            else:
                next_unit['position']['y'] += to_delta[action['direction']]
            next_units.append(next_unit)

        # move enemies
        next_enemies = []
        for enemy in next_board.get_enemies():
            next_enemy = self.move_enemy(enemy)
            next_enemies.append(next_enemy)

        # TODO: apply moves!!

        # assemble board
        next_board.state['units'] = next_units
        next_board.state['enemies'] = next_enemies
        self.current_Board = next_board
        return self.current_Board

    def cell_coords_to_check(self, enemy):
        horizontal_direction = enemy['direction']['horizontal']
        vertical_direction = enemy['direction']['vertical']
        x = enemy['position']['x']
        y = enemy['position']['y']
        return [{'x': x + to_delta[vertical_direction], 'y': y,
                 'direction_if_bounce': {'horizontal': horizontal_direction, 'vertical': flip[vertical_direction]},
                 'next_x': x, 'next_y': y + to_delta[horizontal_direction] * 2},
                {'x': x, 'y': y + to_delta[horizontal_direction],
                 'direction_if_bounce': {'horizontal': flip[horizontal_direction], 'vertical': vertical_direction},
                 'next_x': x + to_delta[vertical_direction] * 2, 'next_y': y}]

    def bounces(self, coords_to_check):
        for coord_to_check in coords_to_check:
            is_bounce = not self.current_Board.can_enemy_attack_coordinates(coord_to_check['x'],
                                                                                  coord_to_check['y'])
            if is_bounce:
                return coord_to_check
        return False

    def move_enemy(self, enemy):
        # check next cell, if nothing there move there
        coords_to_check = self.cell_coords_to_check(enemy)
        bounce = self.bounces(coords_to_check)
        new_enemy = copy.deepcopy(enemy)

        # TODO: corner bounce!

        next_position = {
            'x': new_enemy['position']['x'] + to_delta[enemy['direction']['vertical']],
            'y': new_enemy['position']['y'] + to_delta[enemy['direction']['horizontal']]
        }
        new_enemy['position'] = next_position

        if bounce:
            new_enemy['direction'] = bounce['direction_if_bounce']
            new_enemy['position'] = {'x': bounce['next_x'], 'y': bounce['next_y']}

        return new_enemy
