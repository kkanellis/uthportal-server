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
        self.host = self.settings['host']
        self.max_connections = self.settings['max_connections']

        self._socket = None
        self._server_thread = None
        self._listening = False

        #This holds our open connections' threads
        self._threads = []

        #Flag to signal the server to stop
        self._stop_event = threading.Event()

        self._listening = False

    def listen(self):
        if not self._server_thread:
            #The thread in which our connections are accepted
            self._server_thread = threading.Thread(target = self._serve)
            self._server_thread.daemon = True
            self._server_thread.name = 'server-thread'

        if not self._socket:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.logger.debug("Socket created!")

        if not self._listening:
            try:
                address = (self.host, self.port)
                self.logger.debug("trying to bind on %s:%s" % address)
                self._socket.bind(address)
            except socket.error , msg:
                self.logger.error('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
                self._socket.close()
                return False

            self.logger.debug('Socket bind complete')

            self._socket.listen(self.max_connections)
            self._listening = True
            self.logger.debug("Listening...")

            self._server_thread.start()
            return True

    def stop(self):
        self._stop_event.set()

    def shutdown(self):
        self._stop_event.set()
        for thread in self._threads:
            self.logger.debug("Waiting for thread: [%s]" % thread.name)
            if thread.is_alive():
                self.logger.warn("Kicking connected user.")
                thread.kick()
            thread.join()
        self._socket.close()
        self.logger.info("Socket server shut-down.")

    def _serve(self):
        self.logger.debug("Started server thread: " +
            threading.current_thread().name)
        while not self._stop_event.is_set():
            conn, addr = self._socket.accept()
            self.logger.debug("Connected with %s:%s" % (addr[0], addr[1]))

            this_thread = ClientThread(addr[0], addr[1], conn,
                self.auth_function, self.handle_function, self.logger)
            this_thread.start()
            self._threads.append(this_thread)
        else:
            self._stop_event.clear()
            self._listening = False


class ClientThread(threading.Thread):

    def __init__(self, ip, port, socket, auth, handle, logger):
        super(ClientThread, self).__init__()
        self.ip = ip
        self.port = port
        self.name = "Client: {0}:{1}".format(ip, port)
        socket.settimeout(2)
        self.socket = socket
        self.logger = logger
        self._kick = threading.Event()
        self.logger.debug("New thread spwaned for %s:%s" % (self.ip, self.port))

    def kick(self):
        self.logger.debug("Kick request for %s" % self.name)
        self._kick.set()

    def run(self):
        self.logger.info("[+] Connection from : %s:%s" % (self.ip, self.port))

        self.socket.send("\nWelcome to the server\n\n")

        data = "dummydata"

        while len(data):
            if self._kick.is_set():
                        self.socket.send("You are being kicked!")
                        self.socket.close()
                        self.logger.info("[-] Client on %s:%s kicked." % (self.ip, self.port))
                        return
            try:
                data = self.socket.recv(2048)
                self.socket.send("You sent me : "+data)
            except socket.timeout, e:
                pass

        self.logger.info("[-] Client on %s:%s disconnected." % (self.ip, self.port))
