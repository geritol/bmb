from Game import *
from Board import Board
from Board_settings import *
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

test_simple_board_connect = (Board({
        'cells': [[{'attack': {'can': True}}, {'attack': {'can': True}}],
                  [{'attack': {'can': True}}, {'attack': {'can': True}}]],
        'units': [],
        'enemies': []
    }),
    [],
    Board({
         'cells': [[{'attack': {'can': True}, 'owner': US}, {'attack': {'can': True}, 'owner': US}],
                   [{'attack': {'can': True}, 'owner': US}, {'attack': {'can': True}, 'owner': US}]],
         'units': [],
         'enemies': []
     })
    )

test_simple_board_connect_enemy = (Board({
        'cells': [[{'attack': {'can': True}}, {'attack': {'can': True}}],
                  [{'attack': {'can': True}}, {'attack': {'can': True}}]],
        'units': [],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 1, 'y': 0}}]
    }),
    [],
    Board({
         'cells': [[{'attack': {'can': True}}, {'attack': {'can': True}}],
                   [{'attack': {'can': True}}, {'attack': {'can': True}}]],
         'units': [],
         'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 0, 'y': 1}}]
     })
    )

test_simple_board_connect_enemy_unit = (Board({
        'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}},{'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True, 'unit': US}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True, 'unit': US}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True, 'unit': US}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True, 'unit': US}}, {'attack': {'can': True}}]],
        'units': [{'direction': 'up', 'position': {'y': 3, 'x': 1}, 'killer': 6, 'health': 3, 'owner': US}],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 4, 'y': 0}}]
    }),
    [],
    Board({
        'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}},{'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': False, 'unit': US}}, {'attack': {'can': False, 'unit': US}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': False, 'unit': US}}, {'attack': {'can': False, 'unit': US}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': False, 'unit': US}}, {'attack': {'can': False, 'unit': US}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': False, 'unit': US}}, {'attack': {'can': False, 'unit': US}}]],
        'units': [{'direction': 'up', 'position': {'y': 3, 'x': 0}, 'killer': 6, 'health': 3, 'owner': US}],
         'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 3, 'y': 1}}]
     })
    )

testdata = [
    test_unit_move,
    test_simple_bounce,
    test_simple_board_connect,
    test_simple_board_connect_enemy,
    test_simple_board_connect_enemy_unit
]


@pytest.mark.parametrize('starting_board, actions, expected_board', testdata)
def test_enemy_bounce(starting_board, actions, expected_board):
    next_board = Game(starting_board).move(actions)
    assert next_board.state == expected_board.state
