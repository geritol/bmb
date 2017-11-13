import pytest
from Board import Board
from Board_settings import *


def test_board_scoring_head_collision():
    board = Board({
        'cells': [[{'attack': {'can': True}, 'owner': US}]],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'left'}, 'position': {'x': 0, 'y': 0}}],
        'units': [{'position': {'x': 0, 'y': 0}, 'killer': 6, 'owner': US, 'health': 3, 'direction': 'right'}]
    })
    assert board.evaluate() == SCORE['cell-in-our-possession-multiplier'] + SCORE['head-collision']


testdata = [
    ({'x': -1, 'y': -1}),
    ({'x': -1, 'y': 0}),
    ({'x': 0, 'y': -1}),
    ({'x': 1, 'y': 1}),
    ({'x': 1, 'y': 0}),
    ({'x': 0, 'y': 1}),
]


@pytest.mark.parametrize("position", testdata)
def test_board_scoring_off_board(position):
    board = Board({
        'cells': [[{'attack': {'can': True}, 'owner': US}]],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'left'}, 'position': {'x': 0, 'y': 0}}],
        'units': [{'position': position, 'killer': 6, 'owner': US, 'health': 3, 'direction': 'right'}]
    })
    assert board.evaluate() == SCORE['cell-in-our-possession-multiplier'] + SCORE['off-board']


def test_board_scoring_tail_collision():
    board = Board({
        'cells': [[{'attack': {'can': True}, 'owner': US}, {'attack': {'can': True, 'unit': 0}, 'owner': ENEMY}]],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'left'}, 'position': {'x': 0, 'y': 1}}],
        'units': [{'position': {'x': 0, 'y': 0}, 'killer': 6, 'owner': US, 'health': 3, 'direction': 'right'}]
    })
    assert board.evaluate() == SCORE['cell-in-our-possession-multiplier'] + SCORE['tail-collision']


def test_board_scoring_head_tail_collision():
    board = Board({
        'cells': [[{'attack': {'can': True}, 'owner': US}, {'attack': {'can': True, 'unit': US}, 'owner': ENEMY}, {'attack': {'can': True}, 'owner': ENEMY}]],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'left'}, 'position': {'x': 0, 'y': 2}}],
        'units': [{'position': {'x': 0, 'y': 1}, 'killer': 6, 'owner': US, 'health': 3, 'direction': 'right'}]
    })
    assert board.evaluate() == SCORE['cell-in-our-possession-multiplier'] + SCORE['head-tail-collision']
