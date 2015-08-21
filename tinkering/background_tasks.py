import asyncio, socket

def schedule_coroutine(target, *, loop=None):
    """Schedules target coroutine in the given event loop

    If not given, *loop* defaults to the current thread's event loop

    Returns the scheduled task.
    """
    if asyncio.iscoroutine(target):
        return asyncio.ensure_future(target, loop=loop)
    raise TypeError("target must be a coroutine, "
                    "not {!r}".format(type(target)))

def call_in_background(target, *, loop=None, executor=None):
    """Schedules and starts target callable as a background task

    If not given, *loop* defaults to the current thread's event loop
    If not given, *executor* defaults to the loop's default executor

    Returns the scheduled task.
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    if callable(target):
        return loop.run_in_executor(executor, target)
    raise TypeError("target must be a callable, "
                    "not {!r}".format(type(target)))

def run_in_foreground(task, *, loop=None):
    """Runs event loop in current thread until the given task completes

    Returns the result of the task.
    For more complex conditions, combine with asyncio.wait()
    To include a timeout, combine with asyncio.wait_for()
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    return loop.run_until_complete(asyncio.ensure_future(task, loop=loop))

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

def tcp_echo_client_sync(message, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('-> Client connecting to port: %r' % port)
    conn.connect(('127.0.0.1', port))
    print('-> Client sending: %r' % message)
    conn.send(message.encode())
    data = conn.recv(100).decode()
    print('<- Client received: %r' % data)
    print('-- Terminating connection on client')
    conn.close()
    return data

"""
make_server = asyncio.start_server(handle_tcp_echo, '127.0.0.1')
server = run_in_foreground(make_server)
server.sockets[0]
port = server.sockets[0].getsockname()[1]

make_server2 = asyncio.start_server(handle_tcp_echo, '127.0.0.1')
server2 = run_in_foreground(make_server2)
server2.sockets[0]
port2 = server2.sockets[0].getsockname()[1]

print(run_in_foreground(tcp_echo_client('Hello World!', port)))
print(run_in_foreground(tcp_echo_client('Hello World!', port2)))

echo1 = schedule_coroutine(tcp_echo_client('Hello World!', port))
echo2 = schedule_coroutine(tcp_echo_client('Hello World!', port2))
run_in_foreground(asyncio.wait([echo1, echo2]))
echo1.result()
echo2.result()

query_server = partial(tcp_echo_client_sync, "Hello World!", port)
query_server2 = partial(tcp_echo_client_sync, "Hello World!", port2)
bg_call = call_in_background(query_server)

bg_call2 = call_in_background(query_server2)

run_in_foreground(asyncio.wait([bg_call, bg_call2]))
bg_call.result()
bg_call2.result()
"""


"""
import socket
def blocking_tcp_client(message, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('-> Client connecting to port: {}'.format(port))
    conn.connect(('127.0.0.1', port))
    print('-> Client sending: {!r}'.format(message))
    conn.send(message.encode())
    response = conn.recv(100).decode()
    print('<- Client received: {!r}'.format(response))
    print('-- Terminating connection on client')
    conn.close()
    return response

import asyncio
async def handle_tcp_echo(reader, writer):
    message = (await reader.read(100)).decode()
    print('-> Server received: {!r}'.format(message))
    client = writer.get_extra_info('peername')
    print("<- Server sending {!r} to {}".format(message, client))
    writer.write(message.encode())
    await writer.drain()
    print("-- Terminating connection on server")
    writer.close()

loop = asyncio.get_event_loop()
make_server = asyncio.start_server(handle_tcp_echo, '127.0.0.1')
server = loop.run_until_complete(make_server)
server.sockets
port = server.sockets[0].getsockname()[1]

from functools import partial
query_server = partial(blocking_tcp_client, "Hello World!", port)
background_call = loop.run_in_executor(None, query_server)
response = loop.run_until_complete(background_call)
response

async def tcp_echo_client(message, port):
    reader, writer = await asyncio.open_connection('127.0.0.1', port)
    print('-> Client sending: {!r}'.format(message))
    writer.write(message.encode())
    response = (await reader.read(100)).decode()
    print('<- Client received: {!r}'.format(response))
    print('-- Terminating connection on client')
    writer.close()
    return response

response = loop.run_until_complete(tcp_echo_client('Hello World!', port))
response

def echo_range(stop):
    tasks = (asyncio.ensure_future(tcp_echo_client(str(i), port)) for i in range(stop))
    return asyncio.gather(*tasks)

responses = list(loop.run_until_complete(echo_range(10)))
responses

"""
