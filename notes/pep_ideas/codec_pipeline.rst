Type Neutral Codec API
======================

(Note: this article was substantially rewritten after some initial feedback
from Armin Ronacher. As always, old versions are available on `BitBucket`_)

.. _BitBucket: https://bitbucket.org/ncoghlan/misc/src/default/notes/pep_ideas/codec_pipeline.rst

One of the complaints with Python 3 is that it broke the old idiom for
many text-to-text and binary-to-binary transforms: the ``encode()`` and
``decode()`` methods of 8-bit and Unicode string objects.

In Python 2, these methods were fairly thin shells around the type-neutral
:mod:`codecs` module. Both 8-bit and Unicode strings had both methods and
the type of the return value was based on the specific encoding passed in.

In Python 3, these convenience methods have instead been incorporated
directly into the text model of the language. Text strings only have an
``encode()`` method, and that method can only be used with codecs that
produce bytes objects. Similarly bytes and bytearray objects only have a
``decode()`` method which can only be used with codecs that produce string
objects.


For example (Python 2.7)::

   >>> x = u'Hello World!'.encode("rot-13").encode("koi8-r").encode("bz2")
   >>> x
   'BZh91AY&SY]\xc2\xf0\xb7\x00\x00\x01\x97\x80`\x00\x00\x10\x02\x00\x12\x000  \x001\x06LA\x06\x98\x9a\x166$\x1et\xf1w$S\x85\t\x05\xdc/\x0bp'
   >>> x.decode("bz2").decode("koi8-r").decode("rot-13")
   u'Hello World!'

If you try the first or last step of that chain in Python 3, it fails::

   >>> x = "Hello World!".encode("rot-13").encode("koi8-r").encode("bz2")
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: encoder did not return a bytes object (type=str)
   >>> x = "Hello World!".encode("koi8-r").encode("bz2")
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   AttributeError: 'bytes' object has no attribute 'encode'

This means the old text-to-text and binary-to-binary transforms can only be
accessed via the type neutral :mod:`codecs` module APIs. To make matters
even more annoying, the shorthand aliases for most of those codecs are
`still missing`_, even though the codecs themselves were restored for Python
3.2.

.. _still missing: http://bugs.python.org/issue15331
   
There is `a suggestion`_ that this be replaced directly with a similarly
method-based ``transform``/``untransform`` API, but I'm beginning to wonder
if that's really a good idea. Perhaps it makes more sense to take a step
back and consider a fully type-neutral solution, just like the
:mod:`codecs` module itself.

.. _a suggestion: http://bugs.python.org/issue7475

One very simple alternative, of course, would be a pair of top level
functions in the codecs module that were type neutral alternatives to the
type restricted str and bytes convenience functions::

    def encode(input, encoding, errors='strict'):
        encoder = getencoder(encoding)
        result, len_consumed = encoder(input, errors)
        if len_consumed < len(input):
            # Copy str.encode behaviour for this case
        return result

    def decoder(input, encoding, errors='strict'):
        decoder = getdecoder(encoding)
        result, len_consumed = decoder(input, errors)
        if len_consumed < len(input):
            # Copy bytes.decode behaviour for this case
        return result


Getting Cute with Codec Pipelines
---------------------------------

Armin assures me the following example isn't all that useful in practice,
but it was a fun exercise in exploring what is possible when working
directly with the codecs API.

Below is a sketch of a simple ``CodecPipeline`` that works on both Python 2
and Python 3. It accepts an arbitrary number of codec names as positional
parameters, as well as the error handling scheme as a keyword-only
parameter::

   import codecs
   class CodecPipeline(object):
       """Chains multiple codecs into a single encode/decode operation"""
       def __init__(self, *names, **kwds):
           self.default_errors = self._bind_kwds(**kwds)
           encoders = []
           decoders = []
           self.codecs = names
           for name in names:
               info = self._lookup_codec(name)
               encoders.append(info.encode)
               decoders.append(info.decode)
           self.encoders = encoders
           decoders.reverse()
           self.decoders = decoders

       def _bind_kwds(self, errors=None):
           if errors is None:
               errors = "strict"
           return errors

       def _lookup_codec(self, name):
           # Work around for http://bugs.python.org/issue15331 in 3.x
           try:
               return codecs.lookup(name)
           except LookupError:
               return codecs.lookup(name + "_codec")

       def __repr__(self):
           names = self.codecs
           errors = self.default_errors
           if not names:
               return "{}(errors={!r})".format(type(self).__name__, errors)
           return "{}({}, errors={!r})".format(type(self).__name__,
                                               ", ".join(map(repr, names)),
                                               errors)

       def encode(self, input, errors=None):
           """Apply all encoding operations in the pipeline"""
           if errors is None:
               errors = self.default_errors
           result = input
           for encode in self.encoders:
               result, __ = encode(result, errors)
           return result

       def decode(self, input, errors=None):
           """Apply all decoding operations in the pipeline"""
           if errors is None:
               errors = self.default_errors
           result = input
           for decode in self.decoders:
               result,__ = decode(result, errors)
           return result

And using it in Python 2 looks like this::
    
   >>> cp = CodecPipeline("rot-13", "koi8-r", "bz2")
   >>> cp
   CodecPipeline('rot-13', 'koi8-r', 'bz2', errors='strict')
   >>> cp.encode(u'Hello World!')
   'BZh91AY&SY]\xc2\xf0\xb7\x00\x00\x01\x97\x80`\x00\x00\x10\x02\x00\x12\x000  \x001\x06LA\x06\x98\x9a\x166$\x1et\xf1w$S\x85\t\x05\xdc/\x0bp'
   >>> cp.decode(cp.encode(u'Hello World!'))
   u'Hello World!'

Python 3 looks almost identical, aside from the lack of the ``u`` prefix on
the string literals (and, in Python 3.3, such prefixes are once again legal
on the input front).

   >>> cp = CodecPipeline.from_chain("rot-13", "koi8-r", "bz2")
   >>> cp
   CodecPipeline('rot-13', 'koi8-r', 'bz2', errors='strict')
   >>> cp.encode('Hello World!')
   'BZh91AY&SY]\xc2\xf0\xb7\x00\x00\x01\x97\x80`\x00\x00\x10\x02\x00\x12\x000  \x001\x06LA\x06\x98\x9a\x166$\x1et\xf1w$S\x85\t\x05\xdc/\x0bp'
   >>> cp.decode(cp.encode(u'Hello World!'))
   'Hello World!'

