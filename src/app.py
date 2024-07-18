from .libraries.Strings import *
from .libraries.HTTPInterceptor import HTTPInterceptor, HTTPMapper
from .libraries.HTTPTool import HTTPDetailExtractor
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
            bearerTokens = []

            # different packet commands
            if (self.args.packet_summary):
                Mapper.showSummary(loadedPackets)

            if (self.args.packet_read >= 0):
                Mapper.showPacketDetail(loadedPackets, self.args.packet_read)

            # different bearer commands
            if (self.args.bearer_get):
                HTTPDetailExtractor.extractBearer(loadedPackets, verbose=True)
                return

            if (self.args.bearer_auto):
                bearerTokens = HTTPDetailExtractor.extractBearer(loadedPackets, verbose=True)

            if (self.args.bearer_set):
                bearerTokens = self.args.bearer_set.split(',')

            # different testing methods
            if (self.args.test_repeat):
                Repeater = HTTPRepeaterTest(
                    requestList=loadedPackets,
                    bearerTokens=bearerTokens,
                    statusFilter=self.args.test_status,
                    verbose=self.args.verbose
                )
                Repeater.forward()

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
    ArgParser.add_argument('-tS', '--test-status', metavar='HTTP_STATUS', default='', help=TEST_STATUS_DESCRIPTION)

    # bearer tokens command
    ArgParser.add_argument('-bA', '--bearer-auto', action='store_true', help=AUTO_BEARER_DESCRIPTION)
    ArgParser.add_argument('-bS', '--bearer-set', type=str, metavar='BEARER_TOKENS', help=SET_BEARER_DESCRIPTION)
    ArgParser.add_argument('-bG', '--bearer-get', action='store_true', help=GET_BEARER_DESCRIPTION)

    arguments = ArgParser.parse_args()
    Lazy01(arguments).execute()

    print('[*] Done.', end='\n\n')

    # # test actions
    # ArgParser.add_argument('-tO', '--test-output')
    # ArgParser.add_argument('-tA', '--test-specific')
    # ArgParser.add_argument('-tv', '--test-verbose')

    # # test filters
    # ArgParser.add_argument('-fC', '--filter-code')
    # ArgParser.add_argument('-fE', '--filter-code')

    # ArgParser.add_argument('-bA', '--bearer-auto', action='store_true', help=AUTO_BEARER_DESCRIPTION)