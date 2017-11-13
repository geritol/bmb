"""
simulated_board = {
    board: instance of Board,
    actions: actions taken by our units after the previous state, to achieve this state,
    probability: probability that this state is achieved,
    score: score of this state (board.evaluate()'s output)
}
"""

vertical_to_delta = {
    'left': -1,
    'right': +1
}

horizintal_to_delta = {
    'up': -1,
    'down': +1
}


def cell_coords_to_check(enemy):
    horizontal_direction = enemy['direction']['horizontal']
    vertical_direction = enemy['direction']['vertical']
    x = enemy['position']['x']
    y = enemy['position']['y']
    return [{'x': x + horizintal_to_delta[horizontal_direction], 'y': y},
            {'x':x, 'y': y + vertical_to_delta[vertical_direction]}]


def simulate(simulated_board):
    """
    :param simulated_board: dict, see description
    :return: possible states of the Board in the next tick ([simulated_board1, simulated_board2 ...])
    """
    def move_enemy(enemy):
        # calculate next position
        next_position = {
            'x': horizintal_to_delta[enemy['direction']['horizontal']],
            'y': vertical_to_delta[enemy['direction']['vertical']]
        }

        # check next cell, if nothing there move there
        next_cell = simulated_board.board.get_cell(next_position['x'], next_position['y'])
        if next_cell['attack']['can']:
            return [{
                'direction': enemy['direction'],
                'position': next_position
            }]
        else:


        # if a wall in the way bounce



        # TODO: make bounce logic more sophisticated
        pass

    possible_ = []

    # generate possible moves for units
    for unit in simulated_board.board.get_units():
        possible_unit_actions = []
        for direction in ['up', 'left', 'down', 'right']:
            possible_unit_actions.append({'unit': unit['owner'], 'direction': direction})
        possible_.append(possible_unit_actions)

    # generate possible moves for enemies
    for enemy in simulated_board.board.get_enemies():
        possible_enemy_moves = move_enemy(enemy)
        possible_.append(possible_enemy_moves)
