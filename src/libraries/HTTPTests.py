from .HTTPTool import SimpleHTTPRequestParser
from .Strings import ConsoleStr
import requests as req

class HTTPRepeaterTest:
    def __init__(self,
        requestList: list[SimpleHTTPRequestParser],
        bearerTokens: list[str]=[],
        statusFilter: list=[],
        includePublic: bool=False,
        verbose: bool=False):
            self.requestList = requestList
            self.bearerTokens = bearerTokens
            self.verbose = verbose
            self.statusFilter = statusFilter

            if (includePublic): self.bearerTokens.append('')

    def statusCodePrint(self, statusCode: int):
        if (200 <= statusCode <= 299):
            ConsoleStr.green(str(statusCode))
        elif (400 <= statusCode <= 499):
            ConsoleStr.yellow(str(statusCode))
        elif (500 <= statusCode):
            ConsoleStr.red(str(statusCode))
        else:
            ConsoleStr.blue(str(statusCode))

    def forwarder(self):
        for id, request in enumerate(self.requestList):
            try:
                if (request.method == 'GET'):
                    response = req.get(f'http://{request.host}{request.path}', headers=request.header)
                    if (str(response.status_code) in self.statusFilter or len(self.statusFilter) == 0):
                        ConsoleStr.violet(f'[Repeater GET Test id={id}] Endpoint: {request.path}', end=' |>>> ')
                        self.statusCodePrint(response.status_code)
                        (self.verbose) and ConsoleStr.blue(f'[Response id={id}] {response.text}')
                    continue

                if (request.method == 'DELETE'):
                    response = req.delete(request.path, headers=request.header)
                    if (str(response.status_code) in self.statusFilter or len(self.statusFilter) == 0):
                        ConsoleStr.violet(f'[Repeater DELETE Test id={id}] Endpoint: {request.path}', end=' |>>> ')
                        self.statusCodePrint(response.status_code)
                        (self.verbose) and ConsoleStr.blue(f'[Response id={id}] {response.text}')
                    continue

                if (request.method == 'POST' or request.method == 'PUT'):
                    continue

            except Exception as e:
                print(e)

    def forwardAll(self):
        ConsoleStr.green('========================================')
        ConsoleStr.green('Packet Repeater test')
        ConsoleStr.green('========================================')
        self.forwarder()

    def forwaredAllWithBearer(self):
        # assigning authorization value for each test
        for bearerToken in self.bearerTokens:
            for rid, request in enumerate(self.requestList):

                # safe logic for changing header keys since there are
                # cases where Authorization is in camelcase/lowercase/all-caps
                headerKeys = list(request.header.keys())
                matchHeader = [key.lower() for key in headerKeys]
                if ('authorization' in matchHeader):
                    matchId = matchHeader.index('authorization')
                    actualKey = headerKeys[matchId]
                    self.requestList[rid].header[actualKey] = f'Bearer {bearerToken}'

            # we proceed on overall testing for each bearer tokens
            ConsoleStr.green('\n========================================')
            ConsoleStr.green('Packet Repeater test for token:')
            ConsoleStr.green(f'{bearerToken}')
            ConsoleStr.green('========================================')
            self.forwarder()

    def forward(self):
        if (len(self.bearerTokens) > 0):
            self.forwaredAllWithBearer()
        else:
            self.forwardAll()