Codec Pipelines
===============

One of the complaints with Python 3 is that it broke the old idiom for
implementing codec pipelines: multiple calls to encode and decode methods.

For example (Python 2.7)::

   >>> x = u'Hello World!'.encode("rot-13").encode("koi8-r").encode("bz2")
   >>> x
   'BZh91AY&SY]\xc2\xf0\xb7\x00\x00\x01\x97\x80`\x00\x00\x10\x02\x00\x12\x000  \x001\x06LA\x06\x98\x9a\x166$\x1et\xf1w$S\x85\t\x05\xdc/\x0bp'
   >>> x.decode("bz2").decode("koi8-r").decode("rot-13")
   u'Hello World!'

If you try that in Python 3, it fails::

   >>> x = "Hello World!".encode("rot-13").encode("koi8-r").encode("bz2")

   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: encoder did not return a bytes object (type=str)

I believe that error is on the "rot-13" step, as ``str.encode()`` expects
the codec to emit a bytes objects, but "rot-13" is a text-to-text codec.

There are `some suggestions`_ that this be replaced directly with a similarly
method-based ``transform``/``untransform`` API, but I'm beginning to wonder
if that's really a good idea. Perhaps it makes more sense to take a step
back and consider a fully type-neutral solution, just like the
:mod:`codecs` module itself.

.. _some suggestions: http://bugs.python.org/issue7475

Here's a sketch of a simple ``CodecPipeline`` that works on both Python 2
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

       @classmethod
       def from_chain(cls, codec_chain, errors=None):
           """Create a pipeline from a chain of codec names joined by '+'"""
           names = [name.strip() for name in codec_chain.split("+")]
           return cls(*names, errors=errors)

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
    
   >>> cp = CodecPipeline.from_chain("rot-13+koi8-r+bz2")
   >>> cp
   CodecPipeline('rot-13', 'koi8-r', 'bz2', errors='strict')
   >>> cp.encode(u'Hello World!')
   'BZh91AY&SY]\xc2\xf0\xb7\x00\x00\x01\x97\x80`\x00\x00\x10\x02\x00\x12\x000  \x001\x06LA\x06\x98\x9a\x166$\x1et\xf1w$S\x85\t\x05\xdc/\x0bp'
   >>> cp.decode(cp.encode(u'Hello World!'))
   u'Hello World!'

Python 3 looks almost identical, aside from the lack of the ``u`` prefix on
the string literals (and, in Python 3.3, such prefixes are once again legal
on the input front).

   >>> cp = CodecPipeline.from_chain("rot-13+koi8-r+bz2")
   >>> cp
   CodecPipeline('rot-13', 'koi8-r', 'bz2', errors='strict')
   >>> cp.encode('Hello World!')
   'BZh91AY&SY]\xc2\xf0\xb7\x00\x00\x01\x97\x80`\x00\x00\x10\x02\x00\x12\x000  \x001\x06LA\x06\x98\x9a\x166$\x1et\xf1w$S\x85\t\x05\xdc/\x0bp'
   >>> cp.decode(cp.encode(u'Hello World!'))
   'Hello World!'

