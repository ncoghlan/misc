import threading
import queue

def suspend(*args, **kwds):
    current = threading.current_thread()
    return current.suspend(*args, **kwds)

def cocall(target, *args, **kwds):
    coroutine = CoThread(target)
    return coroutine, coroutine.start(*args, **kwds)

class CoroutineReturn(Exception): pass

class _CoroutineSignal:
    def __init__(self, arg):
        self.arg = arg
   
class CoThread(threading.Thread):

    def __init__(self, target, *args, **kwds):
        kwds["target"] = target
        super().__init__(*args, **kwds)
        self._input = queue.Queue()
        self._output = queue.Queue()
        # Each instance uses unique sentinels to
        # mark special return values
        class RaiseException(_CoroutineSignal): pass
        self._RaiseException = RaiseException
        class ReturnValue(_CoroutineSignal): pass
        self._ReturnValue = ReturnValue

    def run(self):
        try:
            result = self._target(*self._args, **self._kwargs)
        except BaseException as exc:
            self._output.put(self._RaiseException(exc))
        else:
            self._output.put(self._ReturnValue(result))
        finally:
            del self._target, self._args, self._kwargs

    def start(self, *args, **kwds):
        self._args = args
        self._kwargs = kwds
        super().start()
        return self._wait_for_output()

    def join(self, *args):
        try:
            while 1:
                self.resume(*args)
        except CoroutineReturn as result:
            return CoroutineReturn.args[0]

    def _get_data(self, channel):
        data = channel.get()
        if isinstance(data, tuple):
            if not data:
                return None
            if len(data) == 1:
                return data[0]
        return data

    def _wait_for_output(self):
        data = self._get_data(self._output)
        if isinstance(data, self._ReturnValue):
            raise CoroutineReturn(data.arg)
        if isinstance(data, self._RaiseException):
            exc = data.arg
            raise type(exc)(*exc.args) from exc
        return data

    def _check_running(self):
        if not self._started.is_set():
            raise RuntimeError("{!r} not started".format(self))
        if self._stopped:
            raise RuntimeError("{!r} already finished".format(self))
        
    # Whenever we resume a routine, we
    # block until it has data or returns
    def resume(self, *args):
        self._check_running()
        self._input.put(args)
        return self._wait_for_output()

    def throw(self, exc):
        self._check_running()
        self._input.put(self._RaiseException(exc))
        return self._wait_for_output()

    # Whenever we suspend a routine, we
    # block until someone calls resume()
    def suspend(self, *args):
        self._output.put(args)
        data = self._get_data(self._input)
        if isinstance(data, self._RaiseException):
            exc = data.arg
            raise exc
