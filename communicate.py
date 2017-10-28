import socket
import capnp

capnp.remove_import_hook()
request_schema_capnp = capnp.load('./protokoll/Request.capnp')
response_schema_capnp = capnp.load('./protokoll/Response.capnp')
import settings

TCP_DOMAIN = settings.endpoint.split(':')[0]
TCP_PORT = int(settings.endpoint.split(':')[1])
BUFFER_SIZE = 1024


def fixbugs(loggin_info):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_DOMAIN, TCP_PORT))
    s.send(loggin_info.to_bytes())

    data = s.recv(BUFFER_SIZE)
    res = response_schema_capnp.Response.from_bytes(data).to_dict()

    bugs_to_fix = res['bugfix']['bugs']
    bugs_remaining = bugs_to_fix - 1
    finished = False

    while not finished:

        request_payload = request_schema_capnp.Request.new_message()
        bugfix_data = request_payload.init('bugfix')
        bugfix_data.message = 'Fixed'
        bugfix_data.bugs = bugs_remaining
        print('Bugs remaining: {}'.format(bugs_remaining))

        s.send(request_payload.to_bytes())
        res = s.recv(BUFFER_SIZE)
        res = response_schema_capnp.Response.from_bytes(res).to_dict()
        print(res)

        bugs_remaining -= 1

        if 'bugfix' in res and 'message' in res['bugfix']:
            bugs_to_fix = res['bugfix']['bugs']
            bugs_remaining = bugs_to_fix - 1

        if bugs_remaining < 0:
            bugs_remaining = 0

    print(res)
    s.close()
    return data
