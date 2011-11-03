"""urischemes - An extensible URI parsing library

  A URI parsing library that strives to be STD66 (aka RFC3986)
  compliant. http://gbiv.com/protocols/uri/rfc/ has a brief history of
  URI standards, which explains why it took so long to get to where this
  module could be written.

Features:
  * Extensible URI-handling framework that includes default URI parsers
    for many common URI schemes
  * convenience methods for splitting up/rejoining URI references
  * convenience methods for splitting up/rejoining authority strings,
    also known as netloc strings
  * Named tuples URIRef and URIAuthority returned where appropriate
  * convenience methods for splitting up/rejoining URI paths
  * resolve_uriref, which produces an absolute URI given a base URI and a
    relative URI reference to apply

Exposed functions
  - split_uriref, join_uriref, resolve_uriref
  - split_authority, join_authority
  - split_uripath, join_uripath, resolve_uripath
  - split_emailpath, join_emailpath
  - parse_uri

Exposed classes
  - URIRef, URIAuthority, EmailPath
  - SchemeParser, URLSchemeParser, MailtoSchemeParser
  - UnknownSchemeError
  - URIParser

Exposed instances
  - schemes & the sundry scheme parsers it contains
  
Comments:
  * The code looks simple, and you may wonder at the lack of handling
    %-encoding, but STD66 section 2.4 says that %-encodings can't be
    delimiters, so it's okay to be naive.

Usage:
    # Unknown scheme, but provide default authority settings for those
    # schemes where it makes sense
    try:
        pieces = parse_(url, dict(user='user', host='host', port=8080))
    except UnknownSchemeError:
        print 'unknown scheme'

    # if you're trying to parse something with a standard URI scheme 
    # (http for instance), with no default values
    url = "http://user:pass@host:port/path"
    try:
        pieces = http.parse(url)
    except ValueError, ex:
        print ex.message

"""

# Copyright (C) 2006 Nick Coghlan
#  Licensed to Python Software Foundation under a contributor agreement

#  Initially based on Paul Jimenez's uriparse module
#    (Paul's module was posted as http://python.org/sf/1462525)
# Thanks to Mike Brown for pointing out some terminology issues and
#   some major problems with relative URI resolution

#  version 0.4 (8-Jun-2006)
#  version 0.3 (7-Jun-2006)
#  version 0.2 (5-Jun-2006)

# Helper to convert non-strings to strings
def _stringify(item):
    if not isinstance(item, basestring):
        return str(item)
    return item

# Helper for defining tuple subclasses with attributes
class _named_tuple(tuple):
    def __new__(cls, details):
        self = tuple.__new__(cls, details)
        attrs = cls._attrs
        if len(self) != len(attrs):
            raise ValueError('Expected a %d-tuple, got a %d-tuple'
                             % (len(attrs), len(self)))
        for i, attr in enumerate(attrs):
            setattr(self, attr, self[i])
        return self
    def __repr__(self):
        return "%s%r" % (type(self).__name__, tuple(self))



# URI regular expressions based on STD66 aka RFC3986
SCHEME_PATTERN = "(?P<scheme>[^:/?#]+)"
AUTHORITY_PATTERN = "(?P<authority>[^/?#]*)"
PATH_PATTERN = "(?P<path>[^?#]*)"
QUERY_PATTERN = "(?P<query>[^#]*)"
FRAGMENT_PATTERN = "(?P<fragment>.*)"
URI_REFERENCE_PATTERN = (
  "^(%s:)?(//%s)?%s(\?%s)?(#%s)?"
  % (SCHEME_PATTERN, AUTHORITY_PATTERN,
     PATH_PATTERN, QUERY_PATTERN, FRAGMENT_PATTERN)
)

import re as _re
_scheme_match = _re.compile(SCHEME_PATTERN)
_authority_match = _re.compile(AUTHORITY_PATTERN)
_path_match = _re.compile(PATH_PATTERN)
_query_match = _re.compile(QUERY_PATTERN)
_fragment_match = _re.compile(FRAGMENT_PATTERN)
_uri_reference_match = _re.compile(URI_REFERENCE_PATTERN)


# Splitting and joining of URI references

class URIRef(_named_tuple):
    """Tuple subclass to hold URI reference components"""
    _attrs = ('scheme', 'authority', 'path', 'query', 'fragment')
    def __str__(self):
        return join_uriref(self)  

def split_uriref(uriref):
    """
       Basic URI reference parser according to STD66 aka RFC3986

       >>> split_uriref("scheme://authority/path?query#fragment")
       ('scheme', 'authority', 'path', 'query', 'fragment') 

    """
    # Any ASCII string is a legal URI reference
    result = _uri_reference_match.match(uriref)
    return URIRef(result.group(
      'scheme', 'authority', 'path', 'query', 'fragment'))

def join_uriref((scheme, authority, path, query, fragment)):
    """
       Create a URI reference string from its components

       >>> join_uriref('scheme','authority','path','query','fragment')
       "scheme://authority/path?query#fragment"
    """
    pieces = []
    if scheme is not None:
        scheme = _stringify(scheme)
        if _scheme_match.match(scheme) is None:
            raise ValueError("%r is not a valid URI scheme"
                             % (scheme,))
        pieces.append(scheme)
        pieces.append(':')
    if authority is not None:
        authority = _stringify(authority)
        if _authority_match.match(authority) is None:
            raise ValueError("%r is not a valid URI authority"
                             % (authority,))
        pieces.append('//')
        pieces.append(authority)
    if path:
        path = _stringify(path)
        if _path_match.match(path) is None:
            raise ValueError("%r is not a valid URI path"
                             % (path,))
        pieces.append(path)
    if query is not None: 
        query = _stringify(query)
        if _query_match.match(query) is None:
            raise ValueError("%r is not a valid URI query"
                             % (path,))
        pieces.append('?')
        pieces.append(query)
    if fragment is not None:
        # The fragment can be an arbitrary string
        fragment = _stringify(fragment)        
        pieces.append('#')
        pieces.append(fragment)
    return ''.join(pieces)

def resolve_uriref(base, uriref, strict=False):
    """Join a base URI and a (possiby relative) URI reference.
   
    base - base URI
    uriref - a (possibly relative) URI reference to be resolved
    strict - if set to True, an absolute uriref is treated as absolute
             if set to False, an absolute uriref is treated as relative
             when it uses the same scheme as the base uri

    Returns the result as an absolute URI.

    """    
    bscheme, bauthority, bpath, bquery, bfragment = split_uriref(base)
    rscheme, rauthority, rpath, rquery, rfragment = split_uriref(uriref)
    if not strict and (bscheme == rscheme):
        rscheme = None        
    if rscheme is not None:
        # Absolute URI, so ignore base URI
        scheme = rscheme
        authority = rauthority
        path = resolve_uripath(None, rpath)
        query = rquery
    else:
        # Relative reference, so base URI defines scheme
        scheme = bscheme
        if rauthority is not None:
            # Reference defines an authority, so treat as absolute
            authority = rauthority
            path = resolve_uripath(None, rpath)
            query = rquery
        else:
            # Use authority from base URI
            authority = bauthority
            if rpath:
                # Merge paths and use query from URI reference
                path = resolve_uripath(bpath, rpath,
                                       (authority is not None))
                query = rquery
            else:
                # Use path from base URI
                path = bpath
                if rquery is None:
                    # Use query from base URI
                    query = bquery
                else:
                    # Use query from URI reference
                    query = rquery
    # Always use fragment from URI reference
    fragment = rfragment
    # And put it all together
    return join_uriref((scheme, authority, path, query, fragment))


# Splitting and joining of URI authorities

class URIAuthority(tuple):
    """Tuple subclass to hold URI authority components"""
    _attrs = ('user', 'password', 'host', 'port')
    def __str__(self):
        return join_authority(self)  
  
def split_authority(authority):
    """
       Basic authority parser that splits authority into component parts
       
       >>> split_authority("user:password@host:port")
       ('user', 'password', 'host', 'port')

    """
    if '@' in authority:
        userinfo, hostport = authority.split('@', 1)
    else:
        userinfo, hostport = None, authority
    if userinfo and ':' in userinfo:
        user, password = userinfo.split(':', 1)
    else:
        user, password = userinfo, None
    if hostport and ':' in hostport:
        host, port = hostport.split(':', 1)
    else:
        host, port = hostport, None
    if not host:
        host = None
    return URIAuthority((user, password, host, port))


def join_authority((user, password, host, port)):
    """
       Create a URI authority string from its components

       >>> join_authority(('user', 'password', 'host', 'port'))
       "user:password@host:port"

    """
    pieces = []
    if user:
        user = _stringify(user)
        pieces.append(user)
        if password:
            password = _stringify(password)
            pieces.append(':')
            pieces.append(password)
        pieces.append('@')
    host = _stringify(host)
    pieces.append(host)
    if port:
        port = _stringify(port)
        pieces.append(':')
        pieces.append(port)
    authority = ''.join(pieces)
    if _authority_match.match(authority) is None:
        raise ValueError("%r is not a valid URI authority"
                         % (authority,))
    return authority

# Splitting and joining of URI paths

def split_uripath(path):
    """
       Basic URI path parser that splits path into hierarchical segments
       
       >>> split_uripath('/part1/part2/part3/part4')
       ['', 'part1', 'part2', 'part3', 'part4']

    """
    return path.split('/')


def join_uripath(segments):
    """
       Create a URI path string from hierarchical segments

       >>> join_uripath(['', 'part1', 'part2', 'part3', 'part4'])
       '/part1/part2/part3/part4'

    """
    return '/'.join(segments)

def resolve_uripath(bpath, rpath, have_authority=False):
    """
       Create a URI path string from a base path and a relative path

       >>> resolve_uripath('/part1/part2', 'part3/part4')
       '/part1/part2/part3/part4'

    """
    # Merge paths only if base path is defined and rpath is not absolute
    if bpath is None or rpath.startswith('/'):
        input = []
    elif have_authority and bpath == '':
        input = ['']
    else:
        input = split_uripath(bpath)[:-1]
    input.extend(split_uripath(rpath))
    # print "Resolve path input: ", input
    # Remove all dot segments
    input.reverse()
    output = []
    # Strip starting dot segments
    while input and input[-1] in ('.', '..'):
        # Prefix is './' or '../' (item A from RFC)
        # or '.' or '..' is rest of input (item D from RFC)
        # Remove path segment
        input.pop()
    # Handle dot segments within the path
    while input:
        segment = input.pop()
        if segment == '.':
            # Prefix is '/./' (item B from RFC)
            # Replace with '/'
            #   This is implicit unless this is the last input segment
            if not input:
                output.append('')
        elif segment == '..':
            # Prefix is '/../' (item C from RFC)
            # Remove last output segment, 
            #   but don't remove a leading slash!
            if len(output) > 1 or (output and output[0] != ''):
                output.pop()
            # Replace with '/'
            #   This is implicit unless this is the last input segment
            if not input:
                output.append('')
        else:
            # Normal path segment (item E from RFC)
            output.append(segment)
    # print "Resolve path output: ", output
    return join_uripath(output)


# Splitting and joining of email addresses (mailto URI path)
class EmailPath(_named_tuple):
    """Tuple subclass to hold email address URI path components"""
    _attrs = ('user', 'host')
    def __str__(self):
        return join_emailpath(self)

def split_emailpath(path):
    """
       Split an email address into its URI path components
       
       >>> split_uripath('/part1/part2/part3/part4')
       ['', 'part1', 'part2', 'part3', 'part4']

    """
    pieces = path.split('@', 1)        
    if len(pieces) == 2:
        return EmailPath(pieces)
    return EmailPath((path, None))

def join_emailpath((user, host)):
    """
       Create an email address from its components

       >>> join_emailpath(('user', 'host'))
       "user@host"

    """
    if user is None:
        return host
    if host is None:
        return user
    return user + '@' + host

# Define the different classes of scheme parser

class _RelativeRef(_named_tuple):
    """Tuple subclass to hold relative URI reference components"""
    _attrs = ('authority', 'path', 'query', 'fragment')
    def __str__(self):
        return join_uriref(('',) + self)  

class SchemeParser(object):
    """Base class for all scheme-specific URI parsers"""

    def __init__(self, scheme,
                 dauthority=None,
                 dpath='',
                 dquery=None,
                 dfragment=None):
        self.scheme = scheme
        self.defaults = _RelativeRef((dauthority,
                                      dpath,
                                      dquery,
                                      dfragment,
                                    ))

    def parse(self, uriref, defaults=None):
        """Parse a URI reference according to this scheme"""
        scheme, authority, path, query, fragment = split_uriref(uriref)
        dauthority, dpath, dquery, dfragment = self.get_defaults(defaults)
        scheme = self.check_scheme(scheme)
        authority = self.parse_authority(authority, dauthority)
        path = self.parse_path(path, dpath)
        query = self.parse_query(query, dquery)
        fragment = self.parse_fragment(fragment, dfragment)
        return URIRef((scheme, authority, path, query, fragment))

    def get_defaults(self, override):
        """Determine the defaults for a parsing operation"""
        if override is None:
            return self.defaults
        defaults = []
        for name, default in zip(self.defaults._attrs,
                                 self.defaults):
            defaults.append(override.get(name, default))
        return defaults

    def check_scheme(self, scheme):
        """Check a URI scheme is valid for this parser"""
        if not scheme:
            scheme = self.scheme
        elif scheme != self.scheme:
            raise ValueError("%s URI parser cannot handle %s URI"
                             % (self.scheme, scheme))
        return scheme

    def parse_authority(self, authority_str, dauthority=None):
        """Parse the URI authority component according to this scheme"""
        if authority_str is not None:
            authority = split_authority(authority_str)
        else:
            authority = dauthority
        return authority

    def parse_path(self, path_str, dpath=None):
        """Parse the URI path component according to this scheme"""
        if path_str:
            path = path_str
        else:
            path = dpath
        return path

    def parse_query(self, query_str, dquery=None):
        """Parse the URI query component according to this scheme"""
        if query_str is not None:
            query = query_str
        else:
            query = dquery
        return query

    def parse_fragment(self, fragment_str, dfragment=None):
        """Parse the URI fragment component according to this scheme"""
        if fragment_str is not None:
            fragment = fragment_str
        else:
            fragment = dfragment
        return fragment

class URLSchemeParser(SchemeParser):
    """Common parser for all URL style schemes
       scheme://user:password@host:port/path?query#fragment
    """

    def __init__(self, scheme,
                 duser=None,
                 dpassword=None,
                 dhost=None,
                 dport=None,
                 dpath='/',
                 dquery=None,
                 dfragment=None):
        dport = _stringify(dport)
        dauthority = URIAuthority((duser, dpassword,
                                          dhost, dport))
        super(URLSchemeParser, self).__init__(scheme,
                                        dauthority, dpath,
                                        dquery, dfragment)

    def get_defaults(self, override):
        """Determine the defaults for a parsing operation"""
        _get_defaults = super(URLSchemeParser, self).get_defaults
        if override is None or 'authority' in override:
            return _get_defaults(override)
        dauthority = []
        for name, default in zip(self.defaults.authority._attrs,
                                 self.defaults.authority):
            dauthority.append(override.get(name, default))
        override['authority'] = URIAuthority(dauthority)
        return _get_defaults(override)

    def parse_authority(self, authority_str, dauthority=None):
        """Parse the URI authority component according to this scheme"""
        user, password, host, port = split_authority(authority_str)
        duser, dpassword, dhost, dport = dauthority
        if user is None:
            user = duser
        if password is None:
            password = dpassword
        if host is None:
            host = dhost
        if port is None:
            port = dport
        return URIAuthority((user, password, host, port))


class MailtoSchemeParser(SchemeParser):
    """Parser for the mailto URI scheme
       mailto:user@host?query#frag
    """

    def __init__(self, scheme='mailto',
                 duser=None,
                 dhost=None,
                 dquery=None,
                 dfragment=None):
        dpath = EmailPath((duser, dhost))
        super(MailtoSchemeParser, self).__init__(scheme,
                                        None, dpath,
                                        dquery, dfragment)

    def get_defaults(self, override):
        """Determine the defaults for a parsing operation"""
        _get_defaults = super(MailtoSchemeParser, self).get_defaults
        if override is None or 'path' in override:
            return _get_defaults(override)
        dpath = []
        for name, default in zip(self.defaults.path._attrs,
                                 self.defaults.path):
            dpath.append(override.get(name, default))
        override['path'] = EmailPath(dpath)
        return _get_defaults(override)

    def parse_authority(self, authority_str, dauthority=None):
        """Parse the URI authority component according to this scheme"""
        if authority_str is None and dauthority is None:
            return None
        raise ValueError("%s URI parser does not allow authority component"
                          % (self.scheme,))

    def parse_path(self, path_str, dpath=None):
        """Parse the URI path component according to this scheme"""
        duser, dhost = dpath
        if path_str is None:
           user = duser
           host = dhost
        else:
            user, host = split_emailpath(path_str)
            if user is None:
                user = duser
            if host is None:
                host = dhost
        return EmailPath((user, host))

# Define the different schemes

http    = URLSchemeParser('http',
                          dport=80)
https   = URLSchemeParser('https',
                          dport=443)
shttp   = URLSchemeParser('shttp',
                          dport=443)
imap    = URLSchemeParser('imap',
                          dhost='localhost',
                          dport=143)
imaps   = URLSchemeParser('imaps',
                          dhost='localhost',
                          dport=993)
ftp     = URLSchemeParser('ftp',
                          duser='anonymous',
                          dpassword='anonymous',                  
                          dport=21)
tftp    = URLSchemeParser('tftp',
                          dport=69)
file    = URLSchemeParser('file')
telnet  = URLSchemeParser('telnet',
                          dport=23)

mailto  = MailtoSchemeParser()

# Define the scheme independent front end

schemes = dict((x.scheme, x) for x in globals().itervalues()
               if isinstance(x, SchemeParser))

class UnknownSchemeError(KeyError):
    pass
  
class URIParser(object):
    """Scheme-independent parsing frontend

       URIParser is a scheme-conscious parser that picks the right
       parser based on the scheme of the URI handed to it.


    """

    def __init__(self, schemes=schemes, extra={}):
        """Create a new URIParser

        schemes is the full set of schemes to consider.  It defaults to
        urischemes.schemes, which is the full set of known scheme parsers.

        extra is a dictionary of schemename:parserclass that is added to
        the list of known scheme parsers for this URI parser only.

        """
        self._parsers = {}
        self._parsers.update(schemes)
        self._parsers.update(extra)

    def parse(self, uri, defaults=None):
        """Parse the URI.  
        
        uri is the uri to parse (must be an absolute URI).
        defaults is a scheme-dependent dictionary of values to use if there
        is no value for that part in the supplied URI.

        The return value is a URI 5-tuple.

        """
        uri_info = uri.split(':', 1)
        if len(uri_info) == 1:
            raise ValueError("Cannot parse relative URI reference")
        scheme = uri_info[0]
        return self.get_parser(scheme).parse(uri, defaults)

    def get_parser(self, scheme):
        """Return the Parser object used to parse a particular URI.
        
        Parser objects are required to have a 'parse' method.

        """
        try:
            return self._parsers[scheme]
        except KeyError:
            raise UnknownSchemeError(scheme)

_URIParser = URIParser()
parse_uri = _URIParser.parse

def _test():
    import sys
    print "********Testing URI parsing**********"
    parsetests = {
        # Simple tests
        'http://user:pass@host:8080/path?query=result#fragment':
            ('http', ('user', 'pass', 'host', '8080'), '/path', 
                'query=result', 'fragment'),
        'http://user@host:8080/path?query=result#fragment':
            ('http', ('user', None,'host','8080'), '/path',
                'query=result', 'fragment'),
        'http://host:8080/path?query=result#fragment':
            ('http', (None, None, 'host', '8080'), '/path',
                'query=result', 'fragment'),
        'http://host/path?query=result#fragment':
            ('http', (None, None, 'host', '80'), '/path',
                'query=result', 'fragment'),
        'http://host/path?query=result':
            ('http', (None, None, 'host', '80'), '/path',
                'query=result',None),
        'http://host/path#fragment':
            ('http', (None, None, 'host', '80'), '/path',
                None, 'fragment'),
        'http://host/path':
            ('http', (None, None, 'host', '80'), '/path',
                None, None),
        'http://host':
            ('http', (None, None, 'host', '80'), '/',
                None, None),
        'http:///path':
            ('http', (None, None, None, '80'), '/path',
                None, None),
        'tftp:///path':
            ('tftp', (None, None, None, '69'), '/path',
                None, None),
        'mailto:knights@shrubbery.ni':
            ('mailto', None, ('knights', 'shrubbery.ni'),
                None, None),        
        # torture tests
        'http://user:pass@host:port/path?que:ry/res@ult#fr@g:me/n?t': 
            ('http', ('user', 'pass', 'host', 'port'), '/path', 
                'que:ry/res@ult', 'fr@g:me/n?t'),
        'http://user:pass@host:port/path#fr@g:me/n?t': 
            ('http', ('user', 'pass', 'host', 'port'), '/path',
                None, 'fr@g:me/n?t'),
        'http://user:pass@host:port?que:ry/res@ult#fr@g:me/n?t': 
            ('http', ('user', 'pass', 'host', 'port'), '/', 
                'que:ry/res@ult', 'fr@g:me/n?t'),
        'http://user:pass@host:port#fr@g:me/n?t': 
            ('http', ('user', 'pass', 'host', 'port'), '/',
                None, 'fr@g:me/n?t'),
    }
    failures = 0
    for url in parsetests:
        result = parse_uri(url)
        if result != parsetests[url]:
            print ("url: %s : " % url),
            print "Failed."
            print "       got:  %s" % repr(result)
            print "  expected:  %s" % repr(parsetests[url])
            failures += 1

    print "********Testing URI joining from RFC**********"
    base = "http://a/b/c/d;p?q"
    jointests = {     
        # Normal Examples from STD 66 Section 5.4.1
        "g:h"           :  "g:h",
        "g"             :  "http://a/b/c/g",
        "./g"           :  "http://a/b/c/g",
        "g/"            :  "http://a/b/c/g/",
        "/g"            :  "http://a/g",
        "//g"           :  "http://g",
        "?y"            :  "http://a/b/c/d;p?y",
        "g?y"           :  "http://a/b/c/g?y",
        "#s"            :  "http://a/b/c/d;p?q#s",
        "g#s"           :  "http://a/b/c/g#s",
        "g?y#s"         :  "http://a/b/c/g?y#s",
        ";x"            :  "http://a/b/c/;x",
        "g;x"           :  "http://a/b/c/g;x",
        "g;x?y#s"       :  "http://a/b/c/g;x?y#s",
        ""              :  "http://a/b/c/d;p?q",
        "."             :  "http://a/b/c/",
        "./"            :  "http://a/b/c/",
        ".."            :  "http://a/b/",
        "../"           :  "http://a/b/",
        "../g"          :  "http://a/b/g",
        "../.."         :  "http://a/",
        "../../"        :  "http://a/",
        "../../g"       :  "http://a/g",
        # Abnormal Examples from STD 66 Section 5.4.2
        "../../../g"    :  "http://a/g",
        "../../../../g" :  "http://a/g",
        "/./g"          :  "http://a/g",
        "/../g"         :  "http://a/g",
        "g."            :  "http://a/b/c/g.",
        ".g"            :  "http://a/b/c/.g",
        "g.."           :  "http://a/b/c/g..",
        "..g"           :  "http://a/b/c/..g",
        "./../g"        :  "http://a/b/g",
        "./g/."         :  "http://a/b/c/g/",
        "g/./h"         :  "http://a/b/c/g/h",
        "g/../h"        :  "http://a/b/c/h",
        "g;x=1/./y"     :  "http://a/b/c/g;x=1/y",
        "g;x=1/../y"    :  "http://a/b/c/y",
        "g?y/./x"       :  "http://a/b/c/g?y/./x",
        "g?y/../x"      :  "http://a/b/c/g?y/../x",
        "g#s/./x"       :  "http://a/b/c/g#s/./x",
        "g#s/../x"      :  "http://a/b/c/g#s/../x",
        "http:g"        :  "http://a/b/c/g" 
    }

    for relref in jointests:
        result = resolve_uriref(base, relref)
        expected = jointests[relref]
        if result == expected:
            # print "passed"
            pass
        else:
            print "FAILED TEST"
            print "Base:", repr(split_uriref(base))
            print "Ref: ", repr(split_uriref(relref))
            print "Got: ", repr(split_uriref(result))
            print "Want:", repr(split_uriref(expected))
            failures += 1

    print "********Testing URI joining from 4suite**********"
    jointests2 = [
        # Extra test cases from 4suite's tests (courtesy of Mike Brown)
        ('foo:a', 'foo:.', 'foo:'),
        ('zz:abc', 'foo/../../../bar', 'zz:bar'),
        ('zz:abc', '/foo/../../../bar', 'zz:/bar'),
        ('zz:abc', 'zz:.', 'zz:'),
        ('http://a/b/c/d;p?q', 'g/', 'http://a/b/c/g/'),
        ('http://a/b/c/d;p?q', '.', 'http://a/b/c/'),
        ('http://a/b/c/d;p?q', './', 'http://a/b/c/'),
        ('http://a/b/c/d;p?q', '..', 'http://a/b/'),
        ('http://a/b/c/d;p?q', '../', 'http://a/b/'),
        ('http://a/b/c/d;p?q', './g/.', 'http://a/b/c/g/'),
        ('http://a/b/c/d;p?q=1/2', 'g/', 'http://a/b/c/g/'),
        ('http://a/b/c/d;p?q=1/2', './', 'http://a/b/c/'),
        ('http://a/b/c/d;p?q=1/2', '../', 'http://a/b/'),
        ('http://a/b/c/d;p=1/2?q', 'g/', 'http://a/b/c/d;p=1/g/'),
        ('http://a/b/c/d;p=1/2?q', './', 'http://a/b/c/d;p=1/'),
        ('http://a/b/c/d;p=1/2?q', '../', 'http://a/b/c/'),
        ('http://a/b/c/d;p=1/2?q', '../../', 'http://a/b/'),
        ('fred:///s//a/b/c', 'g', 'fred:///s//a/b/g'),
        ('fred:///s//a/b/c', './g', 'fred:///s//a/b/g'),
        ('fred:///s//a/b/c', 'g/', 'fred:///s//a/b/g/'),
        ('fred:///s//a/b/c', '/g', 'fred:///g'),
        ('fred:///s//a/b/c', '///g', 'fred:///g'),
        ('fred:///s//a/b/c', './', 'fred:///s//a/b/'),
        ('fred:///s//a/b/c', '../', 'fred:///s//a/'),
        ('fred:///s//a/b/c', '../g', 'fred:///s//a/g'),
        ('fred:///s//a/b/c', '../../', 'fred:///s//'),
        ('fred:///s//a/b/c', '../../g', 'fred:///s//g'),
        ('fred:///s//a/b/c', '../../../g', 'fred:///s/g'),
        ('fred:///s//a/b/c', '../../../../g', 'fred:///g'),
        ('http:///s//a/b/c', 'g', 'http:///s//a/b/g'),
        ('http:///s//a/b/c', './g', 'http:///s//a/b/g'),
        ('http:///s//a/b/c', 'g/', 'http:///s//a/b/g/'),
        ('http:///s//a/b/c', '/g', 'http:///g'),
        ('http:///s//a/b/c', '///g', 'http:///g'),
        ('http:///s//a/b/c', './', 'http:///s//a/b/'),
        ('http:///s//a/b/c', '../', 'http:///s//a/'),
        ('http:///s//a/b/c', '../g', 'http:///s//a/g'),
        ('http:///s//a/b/c', '../../', 'http:///s//'),
        ('http:///s//a/b/c', '../../g', 'http:///s//g'),
        ('http:///s//a/b/c', '../../../g', 'http:///s/g'),
        ('http:///s//a/b/c', '../../../../g', 'http:///g'),
        ('file:/ex/x/y', 'q/r#', 'file:/ex/x/q/r#'),
        ('file:/some/dir/foo', './#', 'file:/some/dir/#'),
        ('http://example.org/base/uri', 'http:this', 'http:this'),
        ('file:///C:/DEV/Haskell/lib/HXmlToolbox-3.01/examples/',
         'mini1.xml',
         'file:///C:/DEV/Haskell/lib/HXmlToolbox-3.01/examples/mini1.xml'),
    ]
    
    for base, relref, expected in jointests2:
        result = resolve_uriref(base, relref, strict=True)
        if result == expected:
            # print "passed"
            pass
        else:
            print "FAILED TEST"
            print "Base:", repr(split_uriref(base))
            print "Ref: ", repr(split_uriref(relref))
            print "Got: ", repr(split_uriref(result))
            print "Want:", repr(split_uriref(expected))
            failures += 1

    total_tests = len(parsetests)+len(jointests)+len(jointests2)
    print "%d Tests finished." % total_tests
    print "%d failures." % failures
    sys.exit(failures)

if __name__ == '__main__':
    _test()


 	  	 
