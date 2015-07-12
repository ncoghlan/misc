import asyncio

def run_in_background(target, *, loop=None, executor=None):
    """Schedules target as a background task

    Returns the scheduled task.

    If target is a future or coroutine, equivalent to asyncio.ensure_future
    If target is a callable, it is scheduled in the given (or default) executor
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    try:
        return asyncio.ensure_future(target, loop=loop)
    except TypeError:
        pass
    if callable(target):
        return loop.run_in_executor(executor, target)
    raise TypeError("background task must be future, coroutine or "
                    "callable, not {!r}".format(type(target)))

def run_in_foreground(task, *, loop=None):
    """Runs event loop in current thread until the given task completes

    Returns the result of the task.
    For more complex conditions, combine with asyncio.wait()
    To include a timeout, combine with asyncio.wait_for()
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    return loop.run_until_complete(asyncio.ensure_future(task))

async def handle_tcp_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("-> Server received %r from %r" % (message, addr))
    print("<- Server sending: %r" % message)
    writer.write(data)
    await writer.drain()
    print("-- Terminating connection on server")
    writer.close()

async def tcp_echo_client(message, port, loop=None):
    reader, writer = await asyncio.open_connection('127.0.0.1', port, loop=loop)
    print('-> Client sending: %r' % message)
    writer.write(message.encode())
    data = (await reader.read(100)).decode()
    print('<- Client received: %r' % data)
    print('-- Terminating connection on client')
    writer.close()
    return data

"""
make_server = asyncio.start_server(handle_tcp_echo, '127.0.0.1')
server = run_in_foreground(make_server)
port = server.sockets[0].getsockname()[1]

print(run_in_foreground(tcp_echo_client('Hello World!', port)))
"""

