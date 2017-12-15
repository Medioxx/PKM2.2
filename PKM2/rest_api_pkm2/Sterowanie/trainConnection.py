__author__ = 'mikhael'

import socket
import threading
from time import sleep

TCP_IP = '192.168.210.200'
TCP_PORT = 5550
TCP_PORT2 = 5551
BUFFER_SIZE = 1024


class trainClient(object):
    """
    Train TCP Client Class
    """
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket = None
        self.clientAddress = None
        self.connected = False
        self.address = ''
        pass

    def __keepAlive__(self):
        """
        Keeping transmission alive
        """
        while self.connected:
            self.connection.send(b'20 20\r\n')
            # print self.clientSocket.recv(512)
            sleep(5)

    # def __readMsg__(self):
    #     """
    #     Reading data
    #     """
    #     try:
    #
    #         command = ''
    #         while self.connected:
    #             data = self.connection.read()
    #             command += data
    #             if '\r\n' in command:
    #                 print command
    #                 command = ''
    #     except Exception, e:
    #         self.disconnect()

    def __start_reader__(self):
        """
        Start reader thread
        """
        self.receiver_thread = threading.Thread(target=self.__keepAlive__)
        self.receiver_thread.setDaemon(True)
        self.receiver_thread.start()

    def connect(self, address):
        """
        Connect to Lenz TCP/IP Server
        :param address: IP address
        :return:
        """
        self.address = address
        if not self.connected:
            try:
                print('Trying to connect LAN USB')
                self.connection.connect((address, TCP_PORT))
                self.connected = True
                self.__start_reader__()
                print('Connection to LAN USB Server Established')

            except socket.error as msg:
                print('Connection to LAN USB Server Failed')
                print(msg)
                self.connected = False

    def sendMsg(self, msg):
        """
        Sending massage
        :param :msg: massage to send
        :return : received massage
        """
        if self.connected:
            print('Sending IP massage: ' + msg)
            msg = msg.replace('\n', '\r\n')
            self.connection.send(bytes(msg,'utf-8'))
            cc = ''
            for c in self.connection.recv(512).decode():
                if len(hex(int(ord(c)))) == 1:
                    cc += '0'
                cc += hex(int(ord(c)))
            print('Received: ' + cc.replace('0x', ' '))
        #return cc

    def disconnect(self):
        """
        Close connection to TCP/IP server
        """
        if self.connected:
            self.connection.close()
            self.connected = False
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def mushroomStop(self):
        """
        Alarm stop
        """
        self.sendMsg('2180 A1 \r\n')

    def mushroomStart(self):
        """
        Starting after mushroom Stop
        """
        self.sendMsg('2181 A0 \r\n')
