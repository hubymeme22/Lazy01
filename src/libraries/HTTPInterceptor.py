from scapy.all import sniff, Packet, Raw
from scapy.layers.inet import TCP, IP
from scapy.layers.inet6 import IPv6

from .HTTPTool import SimpleHTTPRequestParser, HTTPMapper
from .Strings import ConsoleStr

from dotenv import load_dotenv
import os

load_dotenv()

# A simple class for intercepting http packets
class HTTPInterceptor:
    def __init__(self, port: int, output: str='', verbose: bool=False, unique: bool=False) -> None:
        self.httpPacketState = HTTPMapper(unique)
        self.output = output
        self.verbose = verbose
        self.port = port
        self.count = 1

    def __callbackTemplate(self, httpPacket: Packet):
        if (self.loadedTCPCheck(httpPacket)):
            if (self.targetCheck(httpPacket)):
                ConsoleStr.green(f'[{self.count}] ' + str(httpPacket))
                HTTPPacket = SimpleHTTPRequestParser(httpPacket[Raw].load.decode())
                self.verbose and ConsoleStr.violet(f'[Request] {HTTPPacket.method} {HTTPPacket.path}')
                self.httpPacketState.cacheRequest(HTTPPacket)
            self.count += 1

    def loadedTCPCheck(self, httpPacket: Packet):
        return (httpPacket.haslayer(IP) or httpPacket.haslayer(IPv6)) \
            and httpPacket.haslayer(Raw)

    def targetCheck(self, httpPacket: Packet):
        return httpPacket[TCP].dport == self.port

    def intercept(self, resumePath: str=''):
        ConsoleStr.green(f'[+] Started HTTP Traffic interception for port: {self.port}')
        print('Press CTRL + c to stop intercepting...', end='\n\n')
        sniff(iface=os.getenv('INTERFACE'), filter='tcp', prn=self.__callbackTemplate)

        ConsoleStr.blue('\n[*] Intercepting stopped...')
        if (self.output != ''):
            self.httpPacketState.export(self.output, resumePath)
            ConsoleStr.green(f'[+] Saved as {self.output}', end='\n\n')
            return

        sessionSave = ''
        while True:
            sessionSave = input('Save as new session? [y/N]: ')
            if (sessionSave == 'y' or sessionSave == 'n'):
                break

        if (sessionSave == 'y'):
            fileName = input('Enter filename (*.bka) : ')
            if (len(fileName.split('.')) <= 1):
                fileName += '.bka'
                self.httpPacketState.export(fileName, resumePath)
            ConsoleStr.green(f'[+] Saved as {fileName}', end='\n\n')
        else:
            ConsoleStr.yellow('[*] Quitting...')