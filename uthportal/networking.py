# encoding: utf-8

import socket
import threading
import json
from time import sleep

from logger import get_logger

class ThreadedSocketServer(object):

    def __init__(self, settings):
        self.logger = get_logger('socket_server', settings)
        self.settings = settings['socket_server']

        self._auth_function = None
        self._handle_function = None

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

    def set_handle_function(self, function):
        self._handle_function = function


    def set_auth_function(self, function):
        self._auth_function = function

    def listen(self):
        if not self._server_thread:
            #The thread in which our connections are accepted
            self._server_thread = threading.Thread(target = self._serve)
            self._server_thread.daemon = True
            self._server_thread.name = 'server-thread'

        if not self._socket:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                self._auth_function, self._handle_function, self.logger)
            this_thread.start()
            self._threads.append(this_thread)
        else:
            self._stop_event.clear()
            self._listening = False
            self._server_thread = None


class ClientThread(threading.Thread):
    #Communication is done via json encoded strings
    # auth:{
    #    uname: "username",
    #    passwd: "passwd"
    # }

    # request:{
    #     'cmd' : "command",
    #     'args' : ["arg1", 2, 'arg3']
    # }

    #TODO: maybe use kwargs
    def __init__(self, ip, port, socket, auth, handle, logger):
        super(ClientThread, self).__init__()
        self.ip = ip
        self.port = port
        self.name = "Client: {0}:{1}".format(ip, port)

        self.socket = socket
        #time out the connection on purpose to check for events
        #TODO: maybe find a better way
        socket.settimeout(2)
        self.logger = logger

        self._kick = threading.Event()

        self._handle_function = handle
        self._auth_function = auth

        self._authenticated = False
        self._auth_tries_left = 3

        self.logger.debug("New thread spwaned for %s:%s" % (self.ip, self.port))

    def send_message(self, content, type_ = "info"):
        dict_ = {
                "message":{
                    "content" : content,
                    "type" : type_
                    }
                }
        self.socket.send(json.dumps(dict_))

    def kick(self):
        self.logger.debug("Kick request for %s" % self.name)
        self._kick.set()

    def disconnect(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def _authenticate(self, data):
        try :
            auth_info = json.loads(data)
            auth_info = auth_info["auth"]
            auth_info = [auth_info["uname"], auth_info['passwd']]
            self._authenticated = self._auth_function(auth_info)
            if not self._authenticated:
                self.send_message("Access denied.", "bad")
                self._auth_tries_left -= 1
            else:
                self.send_message("User %s authenticated successfuly.\n" % auth_info[0])
        except ValueError, KeyError:
            self.send_message("Bad authentication data format.", "bad")
            #Prevent auth request spam
            self._auth_tries_left -= 1

            if self._auth_tries_left == 0:
                self._kick.set()

    def _handle_request(self, data):
        try:
            request_info = json.loads(data)
            request_info = request_info['request']
            request_info = [request_info['cmd'], request_info['args']]

            response, type_ = self._handle_function(request_info)
            self.send_message(response, type_)

        except ValueError, KeyError:
            self.send_message("Bad request format", "bad")


    def run(self):
        self.logger.info("[+] Connection from : %s:%s" % (self.ip, self.port))

        self.send_message("Welcome to the UthPortal server!\n\n")

        data = 'dummydata'

        while len(data):
            if self._kick.is_set():
                    self.send_message("Connection termination requested.\n\r")
                    sleep(1)
                    self.disconnect()
                    self.logger.info("[-] Client on %s:%s kicked." % (self.ip, self.port))
                    return
            try:
                data = self.socket.recv(2048)
                data = data.replace("\n","").replace("\r","") #remove ws
                if not self._authenticated:
                    self._authenticate(data)
                    continue #don't handle auth data

                #Auth is ok, handle user data
                self._handle_request(data)
            except socket.timeout, e:
                pass

        self.disconnect()
        self.logger.info("[-] Client on %s:%s disconnected." % (self.ip, self.port))
