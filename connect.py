import capnp
import settings
import Request_capnp

def lambda_print(to_print):
    print(to_print)

client = capnp.TwoPartyClient(settings.endpoint)
request = Request_capnp.Request.new_message()
request.login.team = settings.team
request.login.hash = settings.hash

print("Client: {}".format(client))
print("Request: {}".format(request))

# connecting
temp_request = client.bootstrap().cast_as(request.)
request = temp_request.convert_request()
promise = request.send()
promise.then(lambda ret: lambda_print(ret)).wait()

