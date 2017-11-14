from Game import *
from Board import Board
import pytest

testdata = [
    (Board({
        'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}}]],
        'units': [{'direction': 'down', 'position': {'y': 0, 'x': 0}, 'killer': 6, 'health': 3, 'owner': 1}],
        'enemies': []
    }),
    [{'unit': 0, 'direction': 'right'}],
    Board({
         'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}}]],
         'units': [{'direction': 'right', 'position': {'y': 1, 'x': 0}, 'killer': 6, 'health': 3, 'owner': 1}],
         'enemies': []
     })
    )
]


@pytest.mark.parametrize('starting_board, actions, expected_board', testdata)
def test_enemy_bounce(starting_board, actions, expected_board):
    next_board = Game(starting_board).move(actions)
    assert next_board.state == expected_board.state
