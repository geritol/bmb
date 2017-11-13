from Simulate import *
from Board import Board
import pytest

testdata = [
    ({'board': Board({
        'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}},
                   {'attack': {'can': False}}, {'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True}},
                   {'attack': {'can': False}}, {'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': False}},
                   {'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}},
                   ]],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 1, 'y': 1}}]
        })},
        {'direction': {'vertical': 'down', 'horizontal': 'right'}, 'position': {'x': 1, 'y': 3}}
    )
]


@pytest.mark.parametrize('simulated_board,expected_result', testdata)
def test_enemy_bounce(simulated_board, expected_result):
    next_enemy = move_enemy(simulated_board['board'].get_enemies()[0], simulated_board)
    assert next_enemy == expected_result
