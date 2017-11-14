from Game import *
from Board import Board
import pytest

test_unit_move = (Board({
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

test_simple_bounce = (Board({
        'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}}],
                  [{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True}}]],
        'units': [{'direction': 'down', 'position': {'y': 0, 'x': 0}, 'killer': 6, 'health': 3, 'owner': 1}],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 1, 'y': 1}}]
    }),
    [{'unit': 0, 'direction': 'right'}],
    Board({
         'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}}],
                  [{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True}}]],
         'units': [{'direction': 'right', 'position': {'y': 1, 'x': 0}, 'killer': 6, 'health': 3, 'owner': 1}],
         'enemies': [{'direction': {'vertical': 'down', 'horizontal': 'right'}, 'position': {'x': 1, 'y': 3}}]
     })
    )

testdata = [
    test_unit_move,
    test_simple_bounce
]


@pytest.mark.parametrize('starting_board, actions, expected_board', testdata)
def test_enemy_bounce(starting_board, actions, expected_board):
    next_board = Game(starting_board).move(actions)
    assert next_board.state == expected_board.state
