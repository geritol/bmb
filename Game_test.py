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
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 1, 'y': 0}}]
    }),
    [{'unit': 0, 'direction': 'right'}],
    Board({
         'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}}],
                  [{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True}}]],
         'units': [{'direction': 'right', 'position': {'y': 1, 'x': 0}, 'killer': 6, 'health': 3, 'owner': 1}],
         'enemies': [{'direction': {'vertical': 'down', 'horizontal': 'right'}, 'position': {'x': 1, 'y': 2}}]
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
        'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}},{'attack': {'can': False}}, {'attack': {'can': False}, 'owner': US}, {'attack': {'can': False}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True, 'unit': 0}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True, 'unit': 0}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True, 'unit': 0}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True, 'unit': 0}}, {'attack': {'can': True}}]],
        'units': [{'direction': 'up', 'position': {'y': 3, 'x': 1}, 'killer': 6, 'health': 3, 'owner': US}],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 4, 'y': 0}}]
    }),
    [{'unit': 0, 'direction': 'up'}],
    Board({
        'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}},{'attack': {'can': False}}, {'attack': {'can': False}, 'owner': US}, {'attack': {'can': False}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True}, 'owner': US}, {'attack': {'can': True}, 'owner': US}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True}, 'owner': US}, {'attack': {'can': True}, 'owner': US}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True}, 'owner': US}, {'attack': {'can': True}, 'owner': US}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True}, 'owner': US}, {'attack': {'can': True}, 'owner': US}]],
        'units': [{'direction': 'up', 'position': {'y': 3, 'x': 0}, 'killer': 6, 'health': 3, 'owner': US}],
         'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 3, 'y': 1}}]
     })
    )

test_simple_board_tail = (Board({
        'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}, 'owner': US}, {'attack': {'can': False}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True, 'unit': 0}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True, 'unit': 0}}, {'attack': {'can': True}}]],
        'units': [{'direction': 'up', 'position': {'y': 2, 'x': 2}, 'killer': 6, 'health': 3, 'owner': US}],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 3, 'y': 0}}]
    }),
    [{'unit': 0, 'direction': 'up'}],
    Board({
        'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}, 'owner': US}, {'attack': {'can': False}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True, 'unit': 0}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True, 'unit': 0}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True, 'unit': 0}}, {'attack': {'can': True}}]],
        'units': [{'direction': 'up', 'position': {'y': 2, 'x': 1}, 'killer': 6, 'health': 3, 'owner': US}],
         'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 2, 'y': 1}}]
     })
    )

testdata = [
    test_unit_move,
    test_simple_bounce,
    test_simple_board_connect_enemy,
    test_simple_board_connect_enemy_unit,
    test_simple_board_tail
]


@pytest.mark.parametrize('starting_board, actions, expected_board', testdata)
def test_enemy_bounce(starting_board, actions, expected_board):
    next_board = Game(starting_board).move(actions)
    import pprint
    pprint.pprint(next_board.state)
    pprint.pprint(expected_board.state)
    assert next_board.state == expected_board.state
