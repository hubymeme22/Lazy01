from .libraries.Strings import *
from .libraries.HTTPInterceptor import HTTPInterceptor, HTTPMapper
from .libraries.HTTPTool import HTTPDetailExtractor
from .libraries.HTTPTests import HTTPRepeaterTest
from .auto.loadTokens import loadTokens

import argparse
import os

class Lazy01:
    def __init__(self, arguments: argparse.Namespace) -> None:
        self.args: argparse.Namespace = arguments

    def execute(self):
        if (self.args.retrieve_token):
            loadTokens()

        elif (self.args.intercept):
            if (os.geteuid() != 0):
                ConsoleStr.red('[-] Make sure to run the app as root when calling "--intercept" option.', end='\n\n')
                exit()

            # start intercepting http traffic
            Interceptor = HTTPInterceptor(
                self.args.intercept,
                verbose=self.args.verbose,
                unique=self.args.unique,
                output=self.args.output
            )
            Interceptor.intercept(resumePath=self.args.packet_continue)

        elif (self.args.packet_load):
            bearerTokens = []
            Mapper = HTTPMapper(verbose=self.args.verbose)
            loadedPackets = Mapper.packetLoad(
                self.args.packet_load,
                filter=self.args.packet_method,
                forward=self.args.forward
            )

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
                    includePublic=self.args.test_public,
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

    ArgParser.add_argument('-f', '--forward', type=str, default='', help=FORWARD_DESCRIPTION)
    ArgParser.add_argument('-o', '--output', type=str, default='', help=OUTPUT_DESCRIPTION)
    ArgParser.add_argument('-u', '--unique', action='store_true', help=UNIQUE_DESCRIPTION)
    ArgParser.add_argument('-v', '--verbose', action='store_true', help=VERBOSE_DESCRIPTION)
    ArgParser.add_argument('-i', '--intercept', type=int, default=None, help=INTERCEPT_DESCRIPTION)
    ArgParser.add_argument('-rT', '--retrieve-token', action='store_true', help=RETRIEVE_TOKEN)

    # packet actions
    ArgParser.add_argument('-pC', '--packet-continue', '--packet-resume', metavar='FILE_PATH', type=str, default='', help=PACKET_CONTINUE_DESCRIPTION)
    ArgParser.add_argument('-pL', '--packet-load', metavar='FILE_PATH', type=str, help=PACKET_LOAD_DESCRIPTION)
    ArgParser.add_argument('-pM', '--packet-method', metavar='HTTP_METHOD', type=str, default='', help=PACKET_METHOD_DESCRIPTION)
    ArgParser.add_argument('-pR', '-pD', '--packet-read', metavar='PACKET_ID', type=int , default=-1, help=PACKET_READ_DESCRIPTION)
    ArgParser.add_argument('-pS', '--packet-summary', action='store_true', help=PACKET_SUMMARY_DESCRIPTION)

    # test actions
    ArgParser.add_argument('-tR', '--test-repeat', action='store_true', help=TEST_REPEAT_DESCRIPTION)
    ArgParser.add_argument('-tS', '--test-status', metavar='HTTP_STATUS', default='', help=TEST_STATUS_DESCRIPTION)
    ArgParser.add_argument('-tP', '--test-public', action='store_true', help=TEST_PUBLIC_DESCRIPTION)

    # bearer tokens command
    ArgParser.add_argument('-bA', '--bearer-auto', action='store_true', help=AUTO_BEARER_DESCRIPTION)
    ArgParser.add_argument('-bS', '--bearer-set', type=str, metavar='BEARER_TOKENS', help=SET_BEARER_DESCRIPTION)
    ArgParser.add_argument('-bG', '--bearer-get', action='store_true', help=GET_BEARER_DESCRIPTION)

    arguments = ArgParser.parse_args()
    Lazy01(arguments).execute()

    print('[*] Done.', end='\n\n')

    # test actions
    # TODO: automated login for credentials
    # TODO: token names for labeling instead of showing tokens
    # TODO: proxy for testing
