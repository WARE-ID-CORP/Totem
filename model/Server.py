from socket import *
import logging

class Server():
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.run = True
        self.isReady = False
    
    def serverEthernet(self):
        logging.info("ThreadEthernet - Depart thread socket ethernet")
        self.triggered = False
        self.totemIsReady = True
        cptWithoutResponse = 0
        comSocket = socket(AF_INET, SOCK_STREAM) 
        comSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        comSocket.settimeout(60) 
        try:
            comSocket.bind((self.address, self.port))
            comSocket.listen()
            logging.info("ThreadEthernet - Waiting for client")
            self.eth_client, addr = comSocket.accept()
            logging.info("ThreadEthernet - Client connected")
            self.isReady = True
        except error as exc:
            logging.error("ThreadEthernet - Erreur socket : %s", exc.strerror)
            sleep(5)
            self.serverEthernet()

        while self.run:
            data = self.eth_client.recv(1024)
            logging.info("ThreadEthernet - Data : %s", data)
            if cptWithoutResponse > 5:
                comSocket.shutdown(SHUT_RDWR)
                comSocket.close()
                sleep(5)
                self.serverEthernet()

            if data == b'':
                cptWithoutResponse+=1
                sleep(1)
                continue

            if data == b'2DA3': # Heartbeat
                cptWithoutResponse = 0
                logging.info("ThreadEthernet - Recu Heartbeat")
                message = ''
                if not self.triggered and self.totemIsReady:
                    message = '0241434B3103'
                elif self.triggered and self.totemIsReady:
                    message = '0241434B3203'
                elif self.triggered and not self.totemIsReady:
                    message = '024E414B3103'
                elif not self.triggered and not self.totemIsReady:
                    message = '024E414B3203'
                logging.info("ThreadEthernet - Recu Heartbeat, reponse : %s", message)
                self.sendData(message)
            if data == b'2TOP3': # Trigger
                cptWithoutResponse = 0
                self.triggered = True
                logging.info("ThreadEthernet - Recu Trigger")
                #sleep(self.config["scannerOptions"]["timeBeforeTrigger"])
                #Flash(1, True, False, False, False, False, True)

    def sendData(self, message):
        logging.info("SendMessageToEthernet - Message Hexa : %s", message)
        logging.info("SendMessageToEthernet - Message bytes : %s", bytes.fromhex(message))
        if self.eth_client:
            self.eth_client.send(bytes.fromhex(message))