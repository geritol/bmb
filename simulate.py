import copy
from Game import Game
"""
simulated_board = {
    board: instance of Board,
    actions: actions taken by our units after the previous state, to achieve this state,
    probability: probability that this state is achieved,
    score: score of this state (board.evaluate()'s output)
}
"""

def simulate(simulated_board):
    """
    :param simulated_board: dict, see description
    :return: possible states of the Board in the next tick ([simulated_board1, simulated_board2 ...])
    """

    res = []
    possible_unit_actions = []

    # generate possible moves for units
    for i, unit in enumerate(simulated_board['board'].get_units()):
        possible_unit_action = []
        for direction in ['up', 'left', 'down', 'right']:
            possible_unit_action.append({'unit': i, 'direction': direction, 'position': copy.copy(unit['position'])})
        possible_unit_actions.append(possible_unit_action)

    for possible_unit_action in possible_unit_actions[0]:
        possible_state = {}
        next_board = Game(simulated_board['board']).move([possible_unit_action])
        possible_state['board'] = next_board
        possible_state['actions'] = simulated_board['actions'] + [possible_unit_action]
        possible_state['score'] = next_board.evaluate()
        res.append(possible_state)

    return res
