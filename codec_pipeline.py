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


if __name__ == "__main__":
    # Quick sanity check
   cp = CodecPipeline.from_chain("rot-13+koi8-r+bz2")
   print(cp)
   x = cp.encode('Hello World!')
   print(repr(x))
   print(repr(cp.decode(x)))
