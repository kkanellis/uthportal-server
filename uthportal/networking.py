import socket
import threading
import SocketServer

from logger import get_logger

class ThreadedSocketServer(object):

    def __init__(self, settings):
        self.logger = get_logger('socket_server', settings)
        self.settings = settings['socket_server']

        self.auth_function = None
        self.handle_function = None

        self.port = self.settings['port']
        self.ip = self.settings['ip']
        self.max_connections = self.settingsp['max_connections']

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.debug("Socket created!")

        self.server_thread =

        try:
            address = (self.ip, self.port)
            self.logger.debug("trying to bind on %s:%s" % address)
            s.bind(address)
        except socket.error , msg:
            self.logger.error('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            return

        self.logger.debug('Socket bind complete')
        self._listening = False

    def listen(self):
        if not self._listening:
            self.socket.listen(self.max_connections)
            self._listening = True

    def stop(self):
        self.socket.close
        self._listening = False

class ClientThread(threading.Thread):

    def __init__(self, ip, port, socket, logger):
        super(ClientThread, self).__init__()
        self.ip = ip
        self.port = port
        self.socket = socket
        logger.info("[+] New thread started for "+ip+":"+str(port))


    def __run__(self):
        print "Connection from : "+ip+":"+str(port)

        self.socket.send("\nWelcome to the server\n\n")

        data = "dummydata"

        while len(data):
            data = clientsock.recv(2048)
            print "Client sent : "+data
            self.socket.send("You sent me : "+data)

        print "Client disconnected..."
