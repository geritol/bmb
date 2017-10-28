import capnp

from communicate import fixbugs
import settings

capnp.remove_import_hook()
request_schema_capnp = capnp.load('./protokoll/Request.capnp')

# fill request payload
request_payload = request_schema_capnp.Request.new_message()
login_data = request_payload.init('login')
login_data.team = settings.team
login_data.hash= settings.hash

res = fixbugs(request_payload)
