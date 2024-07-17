from .HTTPTool import SimpleHTTPRequestParser
from .Strings import ConsoleStr
import requests as req

class HTTPRepeaterTest:
    def __init__(self, requestList: list[SimpleHTTPRequestParser], verbose: bool=False):
        self.requestList = requestList

    def statusCodePrint(self, statusCode: int):
        if (200 <= statusCode <= 299):
            ConsoleStr.green(str(statusCode))
        elif (400 <= statusCode <= 499):
            ConsoleStr.yellow(str(statusCode))
        elif (500 <= statusCode):
            ConsoleStr.red(str(statusCode))
        else:
            ConsoleStr.blue(str(statusCode))

    def forwardAll(self, filter=''):
        ConsoleStr.green('========================================')
        ConsoleStr.green('Packet Repeater test')
        ConsoleStr.green('========================================')
        for id, request in enumerate(self.requestList):
            try:
                if (request.method == 'GET'):
                    response = req.get(f'http://{request.host}{request.path}', headers=request.header)
                    ConsoleStr.violet(f'[Repeater Test id={id}] Endpoint: {request.path}', end=' |>>> ')
                    self.statusCodePrint(response.status_code)
                    continue

                if (request.method == 'DELETE'):
                    response = req.delete(request.path, headers=request.header)
                    ConsoleStr.violet('[*] Response Status code:', end=' ')
                    self.statusCodePrint(response.status_code)
                    print()
                    continue

                if (request.method == 'POST' or request.method == 'PUT'):
                    continue

            except Exception as e:
                print(e)
