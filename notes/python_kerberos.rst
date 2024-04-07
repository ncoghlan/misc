Using the Python Kerberos Module
================================

I'm currently integrating Kerberos authentication support into a custom `Pulp`_
client and have completely failed to find any *good* documentation on how
to use the `kerberos`_ module.

I managed to find a `basic example`_, which makes reference to "another
example in the python-kerberos package", which I assume is a reference to
the final `test case`_ in the package. I also looked at the XML-RPC wrapper
implemented in `kobo`_.

Rather than just documenting this for my own use, I decided to write up and
publish what I figured out. Besides, it gives me an excuse to try out
Kenneth Reitz's famous `requests`_ module :)

.. note::

    After I originally wrote this article, Kenneth accepted a `pull request`_
    that added Kerberos authentication support directly to ``requests``. With
    the refactored 1.0 release, that support has been moved out to a separate
    `requests-kerberos`_ project.

All examples in this document are from a Python 2 interactive session.

.. _Pulp: http://pulpproject.org
.. _kerberos: http://pypi.python.org/pypi/kerberos
.. _basic example: http://www.jaddog.org/2009/07/06/python-kerberos-kinit-apache-gssapi-example/
.. _test case: http://trac.calendarserver.org/browser/PyKerberos/trunk/test.py
.. _kobo: http://git.fedorahosted.org/git/?p=kobo.git;a=blob;f=kobo/xmlrpc.py
.. _requests: http://docs.python-requests.org/en/latest/index.html
.. _pull request: https://github.com/kennethreitz/requests/pull/647
.. _requests-kerberos: http://pypi.python.org/pypi/requests-kerberos/


Kerberos Basics
---------------

When setting up Kerberos authentication on a server, there are two basic modes
of operation. The simplest from a client implementation point of view
just uses Basic Auth to pass a username and password to the server, which then
checks them with the Kerberos realm. That's not the case I'm interested in,
since it just looks like ordinary Basic Auth from the client side.

The case I am interested in is the one where the client has a preexisting
Kerberos ticket and we want to pass *that* to the server automatically
without the user needing to reenter their password. The relevant HTTP
authorization protocol is called "Negotiate".

The basic flow of a typical Kerberos authentication is as follows:

* Client sends an unauthenticated request to the server
* Server sends back a 401 response with a ``WWW-Authenticate: Negotiate``
  header with no authentication details
* Client sends a new request with an ``Authorization: Negotiate`` header
* Server checks the ``Authorization`` header against the Kerberos
  infrastructure and either allows or denies access accordingly. If access
  is allowed, it *should* include a ``WWW-Authenticate: Negotiate``
  header with authentication details in the reply.
* Client checks the authentication details in the reply to ensure that the
  request came from the server

This article doesn't cover server side authentication, as I just use
`mod_auth_kerb`_ to handle that side of things and set up the application to
accept the ``REMOTE_USER`` setting from Apache. One useful undocumented trick
that ``mod_auth_kerb`` supports is the `KrbLocalUserMapping`_ option (which
strips the realm details from the value stored in ``REMOTE_USER``).

.. _mod_auth_kerb: http://modauthkerb.sourceforge.net/configure.html
.. _KrbLocalUserMapping: http://serverfault.com/questions/35363/apache-mod-auth-kerb-and-ldap-user-groups


The Role of the Python Kerberos Module
--------------------------------------

From a client point of view, the kerberos module handles two tasks:

  * Figuring out the value to send in the ``Authorization`` field
  * Checking Kerberos level authentication of the response provided by the server

The kerberos module does this by exposing the GSS API - this is an ugly interface,
but it *does* work.


The Initial Request and Response
--------------------------------

This part doesn't involve the kerberos module at all, just a basic HTTP
request::

    >>> import requests
    >>> r = requests.get("https://krbhost.example.com/krb")
    >>> r.status_code
    401
    >>> r.headers["www-authenticate"]
    'Negotiate, Basic realm="Example Realm"'

This example uses a fictional host and realm. This fictional host accepts
either Negotiate (i.e. Kerberos tickets) or direct username/password
authentication.

As the same header occurs multiple times in the response, ``requests`` reports
it as a comma separated list. This isn't very convenient, so we'll write a
helper to split out the auth headers more cleanly::

    >>> def www_auth(response):
    ...     auth_fields = {}
    ...     for field in response.headers.get("www-authenticate", "").split(","):
    ...         kind, __, details = field.strip().partition(" ")
    ...         auth_fields[kind.lower()] = details.strip()
    ...     return auth_fields
    ...
    >>> www_auth(r)
    {'negotiate': '', 'basic': 'realm="Example Realm"'}

That means we can now easily detect when the client should reply with a
Kerberos authenticated connection. For example, a host may provide
two entry points, one configured to use ``mod_auth_kerb`` for
preauthentication of users, while the other handles authentication
entirely at the application level::

    >>> r = requests.get("https://krbhost.example.com/krb/")
    >>> r.status_code == 401 and www_auth(r).get('negotiate') == ''
    True
    >>> r = requests.get("https://krbhost.example.com/api/")
    >>> r.status_code == 401 and www_auth(r).get('negotiate') == ''
    False

If we accessed the ``"https://krbhost.example.com/krb/"`` URL with a
web browser, it would forward the Kerberos ticket if available (and the
browser is configured to do so), otherwise it would pop up a password
dialog, using the realm info from the ``WWW-Authenticate: Basic``
header as the dialog title (at least, that's what Firefox does -
I assume other browsers are similar)


The Kerberos Authenticated Request
----------------------------------

Now we know we want to send a Kerberos authenticated request to the server,
the ``kerberos`` module comes into play. While this is a very thin wrapper
around a C API, it *does* at least turn failures into exceptions (rather
than setting the return code) so we'll ignore that value::

    >>> __, krb_context = kerberos.authGSSClientInit("HTTP@krbhost.example.com")
    >>> kerberos.authGSSClientStep(krb_context, "")
    0
    >>> negotiate_details = kerberos.authGSSClientResponse(krb_context)
    >>> headers = {"Authorization": "Negotiate " + negotiate_details}
    >>> r = requests.get("https://krbhost.example.com/krb/", headers=headers)
    >>> r.status_code
    200
    >>> r.json
    ["example_data"]

You *can* set additional GSS flags in the call to ``authGSSClientInit`` but
I haven't found any need to for simple client authentication via Kerberos.


Authenticating the reply from the server
----------------------------------------

While we can just trust SSL to ensure the integrity of the response from the
server, we can also complete the Kerberos handshake and use it to further
authenticate the reply from the server::

    >>> kerberos.authGSSClientStep(krb_context, www_auth(r)["negotiate"])
    1
    >>> kerberos.authGSSClientClean(krb_context)
    1

As with other calls, these should throw an exception if they fail, so even
though the return code is passed through from C, it should never be anything
other than 1 at the Python level.


Wrapping this up in a helper class
----------------------------------

Here's a simple class that can help make this a bit easier to use in a client
without making any assumptions about the HTTP interface being used::

    class KerberosTicket:
        def __init__(self, service):
            __, krb_context = kerberos.authGSSClientInit(service)
            kerberos.authGSSClientStep(krb_context, "")
            self._krb_context = krb_context
            self.auth_header = ("Negotiate " +
                                kerberos.authGSSClientResponse(krb_context))
        def verify_response(self, auth_header):
            # Handle comma-separated lists of authentication fields
            for field in auth_header.split(","):
                kind, __, details = field.strip().partition(" ")
                if kind.lower() == "negotiate":
                    auth_details = details.strip()
                    break
            else:
                raise ValueError("Negotiate not found in %s" % auth_header)
            # Finish the Kerberos handshake
            krb_context = self._krb_context
            if krb_context is None:
                raise RuntimeError("Ticket already used for verification")
            self._krb_context = None
            kerberos.authGSSClientStep(krb_context, auth_details)
            kerberos.authGSSClientClean(krb_context)

And an example of using it with ``requests``::

    >>> krb = KerberosTicket("HTTP@krbhost.example.com")
    >>> headers = {"Authorization": krb.auth_header}
    >>> r = requests.get("https://krbhost.example.com/krb/", headers=headers)
    >>> r.status_code
    200
    >>> krb.verify_response(r.headers["www-authenticate"])
    >>>
