from .Strings import ConsoleStr
import pathlib
import pickle
import uuid
import os

'''
SimpleHTTPRequestParser

- A simple class for parsing http protocol, specifically made
to retrieve method, host, path, and header contents
'''
class SimpleHTTPRequestParser:
    def __init__(self, request: str) -> None:
        self.errorFlag = None
        self.method = ''
        self.host = ''
        self.path = ''
        self.header = {}

        try:
            # filter to separate body from data
            self.raw = request.replace('\r', '')
            requestDetails = self.raw.split('\n\n')
            requestUri = requestDetails[0].split('\n')
            requestPath = requestUri[0].split(' ')

            # request path details
            self.method = requestPath[0]
            self.path = requestPath[1]
            self.host = requestDetails[0].split('\n')[1:2][0].split(' ')[1]

            # header values parser
            for headerContent in requestDetails[0].split('\n')[2:]:
                headerKeyValue = headerContent.split(': ')
                self.header.update({
                    headerKeyValue[0]: headerKeyValue[1]
                })
        except Exception as e:
            self.errorFlag = e

'''
HTTPMapper

- Class made for saving instances of SimpleHTTPRequest Parser
to storage, this class can be used to save, load, and track
routes that are saved
'''
class HTTPMapper:
    def __init__(self, unique: bool=False) -> None:
        self.fname = f'cache/{uuid.uuid4().hex}.cache'
        self.uniqueFlag = unique
        self.pathMap = {}

    def directCache(self, request: SimpleHTTPRequestParser):
        pathlib.Path(self.fname).touch()
        pickle.dump([request], open(self.fname, 'wb'))
        self.pathMap[request.method + request.path] = True

    def directAppendCache(self, request: SimpleHTTPRequestParser):
        requestList: list = pickle.load(open(self.fname, 'rb'))
        requestList.append(request)
        self.pathMap[request.method + request.path] = True
        pickle.dump(requestList, open(self.fname, 'wb'))

    def cacheRequest(self, request: SimpleHTTPRequestParser):
        (not os.path.isdir('cache')) and os.mkdir('cache')
        if (self.uniqueFlag):
            if ((request.method + request.path) not in self.pathMap):
                (os.path.isfile(self.fname)) and self.directAppendCache(request)
                (not os.path.isfile(self.fname)) and self.directCache(request)
            return
        (os.path.isfile(self.fname)) and self.directAppendCache(request)
        (not os.path.isfile(self.fname)) and self.directCache(request)

    def export(self, filename: str):
        os.replace(self.fname, filename)

    def showSummary(self, filename: str, filter=''):
        requestList: list[SimpleHTTPRequestParser] = pickle.load(open(filename, 'rb'))
        for id, request in enumerate(requestList):
            if (filter == ''):
                ConsoleStr.violet(f'[Request id={id}] {request.method} {request.path}')
                continue
            (request.method == filter) and ConsoleStr.violet(f'[Request id={id}] {request.method} {request.path}')

    def showPacketDetail(self, filename: str, id: int):
        requestList: list[SimpleHTTPRequestParser] = pickle.load(open(filename, 'rb'))
        if (id < len(requestList)):
            targetRequest = requestList[id]
            ConsoleStr.violet(targetRequest.raw)
            print()