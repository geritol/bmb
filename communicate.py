import socket
import capnp
from Board import Board

capnp.remove_import_hook()
request_schema_capnp = capnp.load('./protokoll/Command.capnp')
response_schema_capnp = capnp.load('./protokoll/Response.capnp')
import settings

TCP_DOMAIN = settings.endpoint.split(':')[0]
TCP_PORT = int(settings.endpoint.split(':')[1])
BUFFER_SIZE = 1000000


def connect(loggin_info):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_DOMAIN, TCP_PORT))
    s.send(loggin_info.to_bytes())
    import time
    time.sleep(1)
    data = s.recv(BUFFER_SIZE)

    res = response_schema_capnp.Response.from_bytes(data).to_dict()
    board = Board(res)
    print(board)

    s.close()
    return data
