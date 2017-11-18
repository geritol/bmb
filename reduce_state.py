import json
from Board_settings import *

# number of cells retain (eg. horizontal 3 means  3 cells from the left, 3 from the right will be kept)
HORIZONTAL = 3
VERTICAL = 2

def reduce_state(game_state_input):
    """
    returns reduced state list (one for every units of ours)
    """
    result = []
    game_state = json.loads(json.dumps(game_state_input))

    # place enemies on cells
    for enemy in game_state['enemies']:
        enemy_x = enemy['position']['x']
        enemy_y = enemy['position']['y']
        game_state['cells'][enemy_x][enemy_y]['enemy'] = {
            'direction': enemy['direction']
        }

    # place units on cells
    for unit in game_state['units']:
        unit_x = unit['position']['x']
        unit_y = unit['position']['y']
        game_state['cells'][unit_x][unit_y]['unit'] = True

    # reduce
    for unit in game_state['units']:
        if unit['owner'] != US:
            continue
        unit_x = unit['position']['x']
        unit_y = unit['position']['y']
        res = []
        for row_index in range(unit_x - VERTICAL, unit_x + VERTICAL + 1):
            # if out of bounds add [{}, {}, ...]
            if row_index < 0 or row_index > len(game_state['cells']) - 1:
                row = [{} for _ in range(HORIZONTAL *2 + 1)]
                res.append(row)
                continue
            row = []
            for column_index in range(unit_y - HORIZONTAL, unit_y + HORIZONTAL + 1):
                # if out of bounds add {}
                if column_index < 0 or column_index > len(game_state['cells'][0]) - 1:
                    row.append({})
                    continue
                cell = game_state['cells'][row_index][column_index]
                row.append(cell)
            res.append(row)
        result.append(res)
    return result