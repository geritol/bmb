import socket
import capnp
from Board import Board

capnp.remove_import_hook()
request_schema_capnp = capnp.load('./protokoll/Command.capnp')
response_schema_capnp = capnp.load('./protokoll/Response.capnp')
import settings

TCP_DOMAIN = settings.endpoint.split(':')[0]
TCP_PORT = int(settings.endpoint.split(':')[1])
BUFFER_SIZE = 1024


def connect(loggin_info):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_DOMAIN, TCP_PORT))

    s.send(loggin_info.to_bytes())
    read_socket_data(s)

    res = move(s, [{'unit': 0, 'direction': 'right'}])

    board = Board(res)
    # print(board)
    # print(board.state)
    print(board.state['units'])

    res = move(s, [{'unit': 0, 'direction': 'down'}])
    board = Board(res)
    # print(board)
    # print(board.state)
    print(str(board.evaluate()))

    res = move(s, [{'unit': 0, 'direction': 'right'}])
    board = Board(res)
    #print(board)
    # print(board.state)
    print(board.state['units'])

    res = move(s, [{'unit': 0, 'direction': 'right'}])
    board = Board(res)
    print(board)
    # print(board.state)
    print(board.state['units'])

    while True:
        response = move(s, [{'unit': 0, 'direction': 'down'}])
        print("Response status: {}".format(response['status']))
        board = Board(response)
        print(board)


def move(socket, action_list):
    request_payload = request_schema_capnp.Command.new_message()
    command = request_payload.init('commands')
    moves_data = command.init('moves', 1)
    for i, action in enumerate(action_list):
        move = moves_data[i]
        move.unit = action['unit']
        move.direction = action['direction']
    socket.send(request_payload.to_bytes())

    response = read_socket_data(socket)
    print("Rsponse status: {}".format(response['status']))
    return response


def read_socket_data(socket):
    res = b''

    while True:
        chunk = socket.recv(BUFFER_SIZE)
        res += chunk

        finished = True
        try:
            # read throws error if message is not complete
            response_schema_capnp.Response.from_bytes(res).to_dict()
        except:
            finished = False

        if finished:
            break
    response = response_schema_capnp.Response.from_bytes(res).to_dict()
    print('Response length: {}'.format(len(res)))
    return response
