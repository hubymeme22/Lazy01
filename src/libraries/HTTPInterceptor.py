from scapy.all import sniff, Packet, Raw
from scapy.layers.inet import TCP, IP
from scapy.layers.inet6 import IPv6

from .HTTPTool import SimpleHTTPRequestParser
from .Strings import ConsoleStr

# A simple class for intercepting http packets
class HTTPInterceptor:
    def __init__(self, port: int, verbose: bool=False) -> None:
        self.verbose = verbose
        self.port = port
        self.count = 1

    def __callbackTemplate(self, httpPacket: Packet):
        if (self.loadedTCPCheck(httpPacket)):
            if (self.targetCheck(httpPacket)):
                ConsoleStr.green(f'[{self.count}] ' + str(httpPacket))

                HTTPPacket = SimpleHTTPRequestParser(httpPacket[Raw].load.decode())
                self.verbose and ConsoleStr.violet(f'[Request] {HTTPPacket.method} {HTTPPacket.path}')

                # TODO: write append the packet recieved to save memory
                # TODO: check if unique flag is used here
            self.count += 1

    def loadedTCPCheck(self, httpPacket: Packet):
        return (httpPacket.haslayer(IP) or httpPacket.haslayer(IPv6)) \
            and httpPacket.haslayer(Raw)

    def targetCheck(self, httpPacket: Packet):
        return httpPacket[TCP].dport == self.port

    def intercept(self):
        ConsoleStr.green(f'[+] Started HTTP Traffic interception for port: {self.port}')
        print('Press CTRL + c to stop intercepting...', end='\n\n')
        sniff(iface='lo', filter='tcp', prn=self.__callbackTemplate)

        ConsoleStr.blue('\n[*] Intercepting stopped...')
        if (input('   Save as new session? [y/N]: ') == 'y'):
            fileName = input('   Enter filename (*.bka) : ')
            if (len(fileName.split('.')) <= 1):
                fileName += '.bka'

            # TODO: save file here
            ConsoleStr.green(f'[+] Saved as {fileName}')
            print()
        else:
            ConsoleStr.yellow('[*] Quitting...')