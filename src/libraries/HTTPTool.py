from .Strings import ConsoleStr
import pathlib
import pickle
import glob
import uuid
import json
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
        self.data = None
        self.dataType = None
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

            # data values
            if (requestDetails[-1] != ''): self.data = self.extractJsonContent(requestDetails[-1])
            else: self.data = None
            self.dataType = type(self.data)

        except Exception as e:
            self.errorFlag = e

    def extractJsonContent(self, requestBody: str) -> str | dict:
        try: return json.loads(requestBody)
        except: return requestBody

'''
HTTPMapper

- Class made for saving instances of SimpleHTTPRequest Parser
to storage, this class can be used to save, load, and track
routes that are saved
'''
class HTTPMapper:
    def __init__(self, unique: bool=False, verbose: bool=False) -> None:
        self.fname = f'cache/{uuid.uuid4().hex}.cache'
        self.verbose = verbose
        self.uniqueFlag = unique
        self.pathMap = {}

        verbose and unique and ConsoleStr.green('[*] Unique flag is on (saving unique routes only)')

    def directCache(self, request: SimpleHTTPRequestParser):
        pathlib.Path(self.fname).touch()
        pickle.dump([request], open(self.fname, 'wb'))
        self.pathMap[request.method + request.path] = True

    def directBulkCache(self, requestList: list[SimpleHTTPRequestParser]):
        pathlib.Path(self.fname).touch()
        pickle.dump(requestList, open(self.fname, 'wb'))

        for request in requestList:
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

    def export(self, filename: str, resumepath: str=''):
        if (resumepath != '' and os.path.isfile(resumepath)):
            packet1 = self.packetLoad(self.fname)
            packet2 = self.packetLoad(resumepath)
            self.directBulkCache(packet1 + packet2)

        os.replace(self.fname, filename)

    def packetLoad(self, filename: str, filter: str='', forward: str='') -> list[SimpleHTTPRequestParser]:
        self.verbose and print('[*] Loading packets from', filename)
        requestList: list[SimpleHTTPRequestParser] = []

        if (os.path.isdir(filename)):
            self.verbose and print('[*] Input detected as directory... finding all .bka files')
            fileList = glob.iglob(os.path.join(filename, "*.bka"))

            # loop to retrieve all files
            for file in fileList:
                if (os.path.isfile(file)):
                    self.verbose and print(f'[+] Loading file: {file}')
                    requestList += pickle.load(open(file, 'rb'))

        elif (os.path.isfile(filename)):
            requestList: list[SimpleHTTPRequestParser] = pickle.load(open(filename, 'rb'))
        else:
            ConsoleStr.red(f'[-] The file specified: {filename} does not exist')
            exit()

        filteredRequest = []
        for request in requestList:
            (request.method == filter or filter == '') and filteredRequest.append(request)
            if (forward != ''):
                request.host = forward

        self.verbose and ConsoleStr.green(f'[+] Loaded {len(filteredRequest)} packet(s)')
        return filteredRequest

    def showSummary(self, requestList: list[SimpleHTTPRequestParser]):
        print()
        ConsoleStr.green('========================================')
        ConsoleStr.green(f'{len(requestList)} Packet(s) retrieved:')
        ConsoleStr.green('========================================')

        for id, request in enumerate(requestList):
            ConsoleStr.violet(f'[Request id={id}] {request.method} {request.path}')
        print()

    def showPacketDetail(self, requestList: list[SimpleHTTPRequestParser], id: int):
        if (id < len(requestList)):
            print()
            ConsoleStr.green('========================================')
            ConsoleStr.green(f'Packet detail for id={id}')
            ConsoleStr.green('========================================')
            targetRequest = requestList[id]
            # ConsoleStr.violet(targetRequest.raw)
            ConsoleStr.yellow(f'{targetRequest.method} {targetRequest.path}')
            for key in targetRequest.header.keys():
                ConsoleStr.blue(f'{key}: {targetRequest.header.get(key)}')
            
            if (targetRequest.data != None):
                if (targetRequest.dataType is dict):
                    ConsoleStr.violet(json.dumps(targetRequest.data, indent=2))
                else:
                    ConsoleStr.violet(targetRequest.data)
            print()

class HTTPDetailExtractor:
    def extractBearer(requestList: list[SimpleHTTPRequestParser], verbose: bool=False):
        retrievedKeys = []
        verbose and print('[*] Retrieving all unique bearer tokens...')
        for request in requestList:
            # safe logic for changing header keys since there are
            # cases where Authorization is in camelcase/lowercase/all-caps
            headerKeys = list(request.header.keys())
            matchHeader = [key.lower() for key in headerKeys]
            if ('authorization' in matchHeader):
                matchId = matchHeader.index('authorization')
                actualKey = headerKeys[matchId]
                bearerToken = ' '.join(request.header[actualKey].split(' ')[1:])

                if (bearerToken not in retrievedKeys):
                    verbose and ConsoleStr.green(f'[BearerToken] Retrieved token: {bearerToken}')
                    retrievedKeys.append(bearerToken)

        verbose and print(f'[+] Retrieved {len(retrievedKeys)} bearer tokens')
        return retrievedKeys
