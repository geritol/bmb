import capnp

from communicate import connect
import settings

capnp.remove_import_hook()
request_schema_capnp = capnp.load('./protokoll/Command.capnp')

# fill request payload
request_payload = request_schema_capnp.Command.new_message()
login_data = request_payload.init('commands').init('login')
login_data.team = settings.team
login_data.hash = settings.hash

connect(request_payload)
