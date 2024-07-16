from .libraries.Strings import *
from .libraries.HTTPInterceptor import HTTPInterceptor, HTTPMapper

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

        elif (self.args.packet_summary):
            ConsoleStr.green('=================================')
            ConsoleStr.green('Packets retrieved:')
            ConsoleStr.green('=================================')
            HTTPMapper().showSummary(self.args.packet_summary, filter=self.args.packet_method)
            print('[*] Done.')

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
    ArgParser.add_argument('-pS', '--packet-summary', type=str, help=PACKET_SUMMARY_DESCRIPTION)
    ArgParser.add_argument('-pM', '--packet-method', type=str, default='', help=PACKET_METHOD_DESCRIPTION)

    arguments = ArgParser.parse_args()
    Lazy01(arguments).execute()