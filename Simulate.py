import copy
"""
simulated_board = {
    board: instance of Board,
    actions: actions taken by our units after the previous state, to achieve this state,
    probability: probability that this state is achieved,
    score: score of this state (board.evaluate()'s output)
}
"""

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


def cell_coords_to_check(enemy):
    horizontal_direction = enemy['direction']['horizontal']
    vertical_direction = enemy['direction']['vertical']
    x = enemy['position']['x']
    y = enemy['position']['y']
    return [{'x': x + to_delta[vertical_direction], 'y': y,
             'direction_if_bounce': {'horizontal': horizontal_direction, 'vertical': flip[vertical_direction]},
             'next_x': x, 'next_y': y + to_delta[horizontal_direction] * 2},
            {'x':x, 'y': y + to_delta[horizontal_direction],
             'direction_if_bounce': {'horizontal': flip[horizontal_direction], 'vertical': vertical_direction},
             'next_x': x + to_delta[vertical_direction] * 2, 'next_y': y}]

def bounces(coords_to_check, simulated_board):
    print(coords_to_check)
    for coord_to_check in coords_to_check:
        is_bounce = not simulated_board['board'].can_enemy_attack_coordinates(coord_to_check['x'], coord_to_check['y'])
        if is_bounce:
            return coord_to_check
    return False

def move_enemy(enemy, simulated_board):
    # check next cell, if nothing there move there
    coords_to_check = cell_coords_to_check(enemy)
    bounce = bounces(coords_to_check, simulated_board)
    new_enemy = copy.deepcopy(enemy)

    next_position = {
        'x': new_enemy['position']['x'] + to_delta[enemy['direction']['horizontal']],
        'y': new_enemy['position']['y'] + to_delta[enemy['direction']['vertical']]
    }
    new_enemy['position'] = next_position

    if bounce:
        new_enemy['direction'] = bounce['direction_if_bounce']
        new_enemy['position'] = {'x': bounce['next_x'], 'y': bounce['next_y']}

    return new_enemy


def simulate(simulated_board):
    """
    :param simulated_board: dict, see description
    :return: possible states of the Board in the next tick ([simulated_board1, simulated_board2 ...])
    """

    possible_ = []

    # generate possible moves for units
    for unit in simulated_board['board'].get_units():
        possible_unit_actions = []
        for direction in ['up', 'left', 'down', 'right']:
            possible_unit_actions.append({'unit': unit['owner'], 'direction': direction})
        possible_.append(possible_unit_actions)

    # move enemies
    next_enemies = []
    for enemy in simulated_board['board'].get_enemies():
        next_enemy = move_enemy(enemy)
        next_enemies.append(next_enemy)
