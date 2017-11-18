"""
rl stands for reinforcement learning
"""
import numpy as np
from ddqn import DQNAgent
from Game import Game
from Board import Board
from reduce_state import reduce_state

def move(state, action):
    next_board = Game(Board(state)).move(action)
    score = next_board.evaluate()
    done = False if score else True
    return next_board['state'], score, done, None


state_size = 5000
action_size = 4
agent = DQNAgent(state_size, action_size)
# agent.load("./save/xonix-ddqn.h5")
batch_size = 32


def next_move(state):
    # reduce state
    reduced_states = reduce_state(state)
    moves = []

    for i, reduced_state in enumerate(reduced_states):
        unit_number = i

        action = agent.act(reduced_state)
        print('action:', action)
        next_state, reward, done, _ = move(reduced_state, action)
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)

        moves.append({'unit': unit_number, 'direction': 'right'})

        if done:
            agent.update_target_model()
            print("e: {:.2}"
                  .format(agent.epsilon))
            break

        if len(agent.memory) > batch_size:
            agent.replay(batch_size)
            # if e % 10 == 0:
            #     agent.save("./save/xonix-ddqn.h5")
    return moves
