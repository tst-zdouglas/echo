import thrift
import thrift.protocol.TBinaryProtocol
import thrift.server.TServer
import thrift.transport.TSocket
import echo
import echo.Echo


class Server(object):
    class Handler(object):
        def echo(self, metas):
            return metas

    def start(self):
        proc = echo.Echo.Processor(Server.Handler())
        trans = thrift.transport.TSocket.TServerSocket(host='localhost',
                                                       port=9999)
        tfact = thrift.transport.TTransport.TBufferedTransportFactory()
        pfact = thrift.protocol.TBinaryProtocol. \
            TBinaryProtocolAcceleratedFactory()
        thrift.server.TServer.TForkingServer(proc, trans, tfact, pfact).serve()


def ping():
    def vtyp(n):
        if n % 2:
            if n % 3:
                return str(n)
            else:
                return bool(n)
        else:
            return -n
    trans = thrift.transport.TSocket.TSocket(
        'localhost', 9999
    )
    trans = thrift.transport.TTransport. \
        TBufferedTransport(trans)
    prot = thrift.protocol.TBinaryProtocol. \
        TBinaryProtocolAccelerated(trans)
    client = echo.Echo.Client(prot)
    trans.open()
    metas = [
        echo.ttypes.Meta(
            k=str(n),
            t=n,
            v=str(vtyp(n))
        )
        for n
        in xrange(6)
    ]
    print metas
    print client.echo(
        metas=metas
    )
    trans.close()

if __name__ == '__main__':
    import os
    import signal
    import time
    pid = os.fork()
    if pid:
        time.sleep(3)
        ping()
        os.kill(pid, signal.SIGKILL)
    Server().start()
