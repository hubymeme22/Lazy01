from .libraries.Strings import *
from .libraries.HTTPInterceptor import HTTPInterceptor, HTTPMapper
from .libraries.HTTPTests import HTTPRepeaterTest

import argparse
import os

class Lazy01:
    def __init__(self, arguments: argparse.Namespace) -> None:
        self.args: argparse.Namespace = arguments

    def execute(self):
        if (self.args.intercept):
            if (os.geteuid() != 0):
                ConsoleStr.red('[-] Make sure to run the app as root when calling "--intercept" option.', end='\n\n')
                exit()

            # start intercepting http traffic
            Interceptor = HTTPInterceptor(self.args.intercept, verbose=self.args.verbose, unique=self.args.unique)
            Interceptor.intercept()

        elif (self.args.packet_load):
            Mapper = HTTPMapper(verbose=self.args.verbose)
            loadedPackets = Mapper.packetLoad(self.args.packet_load, filter=self.args.packet_method)

            if (self.args.packet_summary):
                Mapper.showSummary(loadedPackets)

            if (self.args.packet_read >= 0):
                Mapper.showPacketDetail(loadedPackets, self.args.packet_read)

            if (self.args.test_repeat):
                Repeater = HTTPRepeaterTest(loadedPackets)
                Repeater.forwardAll()

            print('[*] Done.')
            print()

        else:
            print('usage: lazy01.py [options]')
            print('you can use -h or --help for additional options ', end='\n\n')

def start():
    ConsoleStr.green(ASCII_ART)
    print()

    ArgParser = argparse.ArgumentParser(description=APP_DESCRIPTION)

    ArgParser.add_argument('-u', '--unique', action='store_true', help=UNIQUE_DESCRIPTION)
    ArgParser.add_argument('-v', '--verbose', action='store_true', help=VERBOSE_DESCRIPTION)
    ArgParser.add_argument('-i', '--intercept', type=int, default=None, help=INTERCEPT_DESCRIPTION)

    # packet actions
    ArgParser.add_argument('-pL', '--packet-load', metavar='FILE_PATH', type=str, help=PACKET_LOAD_DESCRIPTION)
    ArgParser.add_argument('-pM', '--packet-method', metavar='HTTP_METHOD', type=str, default='', help=PACKET_METHOD_DESCRIPTION)
    ArgParser.add_argument('-pR', '-pD', '--packet-read', metavar='PACKET_ID', type=int , default=-1, help=PACKET_READ_DESCRIPTION)
    ArgParser.add_argument('-pS', '--packet-summary', action='store_true', help=PACKET_SUMMARY_DESCRIPTION)

    # test actions
    ArgParser.add_argument('-tR', '--test-repeat', action='store_true', help=TEST_REPEAT_DESCRIPTION)

    arguments = ArgParser.parse_args()
    Lazy01(arguments).execute()

    # # test actions
    # ArgParser.add_argument('-tO', '--test-output')
    # ArgParser.add_argument('-tA', '--test-specific')
    # ArgParser.add_argument('-tv', '--test-verbose')

    # # test filters
    # ArgParser.add_argument('-fC', '--filter-code')
    # ArgParser.add_argument('-fE', '--filter-code')

    # # modification actions
    # ArgParser.add_argument('-sA', '--set-authority')
    # ArgParser.add_argument('-sC', '--set-cookie')

