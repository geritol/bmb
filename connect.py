import capnp
import settings

capnp.remove_import_hook()
request_capnp = capnp.load('./protokoll/Request_interface.capnp')
request_schema_capnp = capnp.load('./protokoll/Request.capnp')

# fill request payload
request_payload = request_schema_capnp.Request.new_message()
login_data = request_payload.init('login')
login_data.team = settings.team
login_data.hash= settings.hash

print(request_payload)

# connect to the server
client = capnp.TwoPartyClient(settings.endpoint).bootstrap().cast_as(request_capnp.Req)
request = client.login(request_payload)

print(request)

r = request.then(lambda ret: ret.value.read()).wait()

# getting the following from the server:
# capnp.lib.capnp.KjException: capnp/layout.c++:2154: disconnected: expected ref->kind() == WirePointer::STRUCT;
# Message contains non-struct pointer where struct pointer was expected.
# ---- or ----
# capnp.lib.capnp.KjException: capnp/rpc.c++:2092: disconnected: Peer disconnected.

print(r)