from .libraries.Strings import *
from .libraries.HTTPInterceptor import HTTPInterceptor

import argparse
import os

class Lazy01:
    def __init__(self, arguments: argparse.Namespace) -> None:
        self.args: argparse.Namespace = arguments
        self.port: int = arguments.PORT
        (self.port == None) and exit()

    def execute(self):
        if (self.args.intercept):
            if (os.geteuid() != 0):
                ConsoleStr.red('[-] Make sure to run the app as root when calling "--intercept" option.', end='\n\n')
                exit()

            # start intercepting http traffic
            Interceptor = HTTPInterceptor(self.port, verbose=self.args.verbose)
            Interceptor.intercept()

        else:
            print('usage: lazy01 <port> [options]')
            print('you can use -h or --help for additional options ', end='\n\n')

def start():
    ConsoleStr.green(ASCII_ART)
    print()

    ArgParser = argparse.ArgumentParser(description=APP_DESCRIPTION)
    ArgParser.add_argument('PORT', type=int, help=PORT_DESCRIPTIOM)

    ArgParser.add_argument('-i', '--intercept', action='store_true', help=INTERCEPT_DESCRIPTION)
    ArgParser.add_argument('-u', '--unique', action='store_true', help=UNIQUE_DESCRIPTION)
    ArgParser.add_argument('-v', '--verbose', action='store_true', help=VERBOSE_DESCRIPTION)

    arguments = ArgParser.parse_args()
    Lazy01(arguments).execute()