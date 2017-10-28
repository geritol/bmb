@0xecc23a6ce1dbd596;

# using Java = import "java.capnp";
# $Java.package("org.ericsson2017.protocol.test");
# $Java.outerClassname("RequestClass");

# using Cxx = import "/capnp/c++.capnp";
# $Cxx.namespace("ericsson2017::protocol::test");

using import "Bugfix.capnp".Bugfix;
using import "Response.capnp".Response;
using import "Request.capnp".Request;

interface Req{
    login @0 (expression: Request) -> (response: Response);
}
