import capnp
import settings

capnp.remove_import_hook()
request_capnp = capnp.load('./protokoll/Request.capnp')
client = capnp.TwoPartyClient(settings.endpoint)
