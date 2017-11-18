from reduce_state import *
import pytest
import pprint

test_border = ({
        'cells': [[{'attack': {'can': False}}, {'attack': {'can': False}},{'attack': {'can': False}}, {'attack': {'can': False}}, {'attack': {'can': False}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True}}, {'attack': {'can': True}}],
                [{'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True, 'unit': 0}}, {'attack': {'can': True}}]],
        'units': [{'direction': 'up', 'position': {'y': 0, 'x': 0}, 'killer': 6, 'health': 3, 'owner': US}],
        'enemies': [{'direction': {'vertical': 'up', 'horizontal': 'right'}, 'position': {'x': 0, 'y': 1}}]
    },
    [[[{}, {}, {}, {}, {}, {}, {}],
      [{}, {}, {}, {}, {}, {}, {}],
      [{}, {}, {}, {'attack': {'can': False}, 'unit': True}, {'attack': {'can': False}, 'enemy': {'direction': {'horizontal': 'right', 'vertical': 'up'}}},{'attack': {'can': False}}, {'attack': {'can': False}}],
      [{}, {}, {}, {'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True}}],
      [{}, {}, {}, {'attack': {'can': True}}, {'attack': {'can': True}},{'attack': {'can': True}}, {'attack': {'can': True}}]
      ]]
    )

testdata = [
    test_border
]


@pytest.mark.parametrize('starting_state, expected_state', testdata)
def test_reduce(starting_state, expected_state):
    reduced_state = reduce_state(starting_state)
    pprint.pprint(reduced_state)
    pprint.pprint(expected_state)
    assert reduced_state == expected_state
