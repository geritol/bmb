"""
rl stands for reinforcement learning
"""
import numpy as np
from ddqn import DQNAgent
from Game import Game
from Board import Board
from reduce_state import reduce_state

PENALTY_PER_MOVE = -3
STARTING_SCORE = 7040
FILE_NAME = "./save/xonix-ddqn.h5"

# TODO: rewrit this oop style

empty_state = [[{}, {}, {}, {}, {}, {}, {}],
                [{}, {}, {}, {}, {}, {}, {}],
                [{}, {}, {}, {}, {}, {}, {}],
                [{}, {}, {}, {}, {}, {}, {}],
                [{}, {}, {}, {}, {}, {}, {}],
               ]

def move(state, action, move_count):
    next_board = Game(Board(state)).move(action)
    print(next_board)
    if next_board:
        score = next_board.evaluate() - STARTING_SCORE + PENALTY_PER_MOVE * move_count
        print('SCORE: {}'.format(score))
        return convert_to_list(reduce_state(next_board.state)[action[0]['unit']]), score, False, None
    else:
        score = -10000
        return convert_to_list(empty_state), score, True, None


def convert_to_list(state):
    res = []
    for line in state:
        for cell in line:
            if 'attack' in cell:
                if 'can' in cell['attack']:
                    res.append(1)
                else:
                    res.append(0)
                if 'unit' in cell['attack']:
                    res.append(cell['attack']['unit'])
                else:
                    res.append(10000)
            else:
                res.append(10000)
                res.append(10000)
            if 'owner' in cell:
                res.append(cell['owner'])
            else:
                res.append(10000)
            if 'unit' in cell:
                res.append(1)
            else:
                res.append(10000)
            if 'enemy' in cell:
                res.append(1)
                res.append(directions_back[cell['enemy']['direction']['horizontal']])
                res.append(directions_back[cell['enemy']['direction']['vertical']])
            else:
                res.append(10000)
                res.append(10000)
                res.append(10000)
    return res


state_size = 245
action_size = 4
agent = DQNAgent(state_size, action_size)
#agent.load(FILE_NAME)
batch_size = 32

derections = {
    0: 'up',
    1: 'left',
    2: 'down',
    3: 'right'
}

directions_back = {
    'up': 0,
    'left': 1,
    'down': 2,
    'right': 3
}


def next_move(state, move_count):
    # reduce state
    reduced_states = reduce_state(state)
    moves = []

    for i, reduced_state in enumerate(reduced_states):
        unit_number = i

        r_state = np.reshape(convert_to_list(reduced_state), [1, state_size])
        action = agent.act(r_state)
        action = derections[action]
        print('action:', action)
        next_state, reward, done, _ = move(state, [{'unit': unit_number, 'direction': action}], move_count)
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(r_state, directions_back[action], reward, next_state, done)

        moves.append({'unit': unit_number, 'direction': action})

        if done:
            agent.update_target_model()
            print("e: {:.2}"
                  .format(agent.epsilon))
            agent.save(FILE_NAME)

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
            agent.save(FILE_NAME)
    return moves
