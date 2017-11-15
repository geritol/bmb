import copy
from Board_settings import *

to_delta = {
    'left': -1,
    'right': +1,
    'up': -1,
    'down': +1
}

flip = {
    'left': 'right',
    'right': 'left',
    'up': 'down',
    'down': 'up'
}

class Game:
    def __init__(self, starting_Board):
        self.starting_Board = starting_Board
        self.current_Board = starting_Board

    def move(self, action_list):
        """
        Applies the actions to self.current_Board, and returns the new Board
        """
        next_board = copy.deepcopy(self.current_Board)

        # move units
        next_units = []
        for action in action_list:
            next_unit = copy.deepcopy(next_board.get_units()[action['unit']])
            next_unit['direction'] = action['direction']
            if action['direction'] in ['up', 'down']:
                next_unit['position']['x'] += to_delta[action['direction']]
            else:
                next_unit['position']['y'] += to_delta[action['direction']]
            next_units.append(next_unit)

        # move enemies
        next_enemies = []
        for enemy in next_board.get_enemies():
            next_enemy = self.move_enemy(enemy)
            next_enemies.append(next_enemy)

        # TODO: apply moves!!
        # check if unit dies or not

        # check if unit ends up on a 'safe space'
        # if yes, mark tail as safe

        # if not dead, gather connected empty cells
        # check if connections have units
        # if no enemy on the connected cells, mark as owned by us
        connected_empty_cell_coordinates = self.get_connected_empty_cell_coordinate()
        print(connected_empty_cell_coordinates)
        for connected_cordinates in connected_empty_cell_coordinates:
            no_enemy = True
            for cordinates in connected_cordinates:
                if self.current_Board.cell_has_enemy(*cordinates):
                    no_enemy = False
                    break
            if no_enemy:
                # mark cells as possessed by us
                for cordinates in connected_cordinates:
                    cell = next_board.get_cell(*cordinates)
                    cell['owner'] = US

        # assemble board
        next_board.state['units'] = next_units
        next_board.state['enemies'] = next_enemies
        self.current_Board = next_board
        return self.current_Board

    def get_connected_empty_cell_coordinate(self):
        result = []
        visited_cells = {}
        for i, line in enumerate(self.current_Board.state['cells']):
            for j in range(len(line)):
                coordinates_to_check = [[i, j]]
                connected = []
                while len(coordinates_to_check) > 0:
                    print('cords to check: ', coordinates_to_check)
                    current = coordinates_to_check.pop()
                    cell = self.current_Board.get_cell(*current)
                    if str(current) in visited_cells:
                        continue
                    if not cell['attack']['can']:
                        continue
                    connected.append(current)
                    visited_cells[str(current)] = True
                    coordinates_to_check += self.get_neighbor_cell_coordinate(*current)
                    print('cords to check: (2) ', coordinates_to_check)
                    print(connected)
                if connected:
                    result.append(connected)
        return result

    def get_neighbor_cell_coordinate(self, x, y):
        result = []
        width = self.current_Board.width
        height = self.current_Board.height
        for x_delta in [-1, 0, 1]:
            for y_delta in [-1, 0, 1]:
                neighbor_x = x + x_delta
                neighbor_y = y + y_delta
                if x_delta != 0 and y_delta != 1:
                    continue
                if 0 > neighbor_x or neighbor_x > height - 1:
                    continue
                if 0 > neighbor_y or neighbor_y > width - 1:
                    continue
                result.append([neighbor_x, neighbor_y])
        return result

    def cell_coords_to_check(self, enemy):
        horizontal_direction = enemy['direction']['horizontal']
        vertical_direction = enemy['direction']['vertical']
        x = enemy['position']['x']
        y = enemy['position']['y']
        return [{'x': x + to_delta[vertical_direction], 'y': y,
                 'direction_if_bounce': {'horizontal': horizontal_direction, 'vertical': flip[vertical_direction]},
                 'next_x': x, 'next_y': y + to_delta[horizontal_direction] * 2},
                {'x': x, 'y': y + to_delta[horizontal_direction],
                 'direction_if_bounce': {'horizontal': flip[horizontal_direction], 'vertical': vertical_direction},
                 'next_x': x + to_delta[vertical_direction] * 2, 'next_y': y}]

    def bounces(self, coords_to_check):
        for coord_to_check in coords_to_check:
            is_bounce = not self.current_Board.can_enemy_attack_coordinates(coord_to_check['x'],
                                                                                  coord_to_check['y'])
            if is_bounce:
                return coord_to_check
        return False

    def move_enemy(self, enemy):
        # check next cell, if nothing there move there
        coords_to_check = self.cell_coords_to_check(enemy)
        bounce = self.bounces(coords_to_check)
        new_enemy = copy.deepcopy(enemy)

        # TODO: corner bounce!

        next_position = {
            'x': new_enemy['position']['x'] + to_delta[enemy['direction']['vertical']],
            'y': new_enemy['position']['y'] + to_delta[enemy['direction']['horizontal']]
        }
        new_enemy['position'] = next_position

        if bounce:
            new_enemy['direction'] = bounce['direction_if_bounce']
            new_enemy['position'] = {'x': bounce['next_x'], 'y': bounce['next_y']}

        return new_enemy
