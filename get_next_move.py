from Board import Board
from simulate import simulate

total_calls = 0

def get_next_move(state, max_depth):
    board = Board(state)
    simulated = {
        'board': board,
        'actions': [],
        'probability': 100,
        'score': board.evaluate()
    }
    res = get_moves(simulated, 1, max_depth)
    print(res)
    return res[1]


def get_moves(simulated_board, current_depth, max_depth):
    global total_calls
    total_calls +=1
    if current_depth > max_depth:
        return simulated_board['score'], simulated_board['actions']

    results = []
    next_up = simulate(simulated_board)
    for next in next_up:
        res = get_moves(next, current_depth + 1, max_depth)
        results.append(res)
    return sorted(results, key=lambda l:l[0], reverse=True)[0]




