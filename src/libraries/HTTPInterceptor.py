from scapy.all import sniff, Packet, Raw
from scapy.layers.inet import TCP, IP
from scapy.layers.inet6 import IPv6
from .Strings import ConsoleStr

# a simple class for intercepting http packets
class HTTPInterceptor:
    def __init__(self, port: int, verbose: bool=False) -> None:
        self.verbose = verbose
        self.port = port
        self.count = 1

    def __callbackTemplate(self, httpPacket: Packet):
        if (self.loadedTCPCheck(httpPacket)):
            if (self.targetCheck(httpPacket)):
                ConsoleStr.green(f'[{self.count}] ' + str(httpPacket))
            else:
                ConsoleStr.blue(f'[{self.count}] ' + str(httpPacket))
            self.count += 1

    def loadedTCPCheck(self, httpPacket: Packet):
        return (httpPacket.haslayer(IP) or httpPacket.haslayer(IPv6)) \
            and httpPacket.haslayer(Raw)

    def targetCheck(self, httpPacket: Packet):
        return httpPacket[TCP].dport == self.port

    def intercept(self):
        ConsoleStr.green(f'[+] Started HTTP Traffic interception for port: {self.port}', end='\n\n')
        sniff(iface='lo', filter='tcp', prn=self.__callbackTemplate)