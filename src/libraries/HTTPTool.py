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
    def __init__(self, unique=False) -> None:
        self.uniqueFlag = unique
        self.pathMap = {}
        self.id = str(uuid.uuid4().hex)

    def cacheRequest(self, request: SimpleHTTPRequestParser):
        (not os.path.isdir('cache')) and os.mkdir('cache')
        if (self.uniqueFlag):
            if (request.path not in self.pathMap):
                fname = f'cachce/{self.id}.cache'
                if (os.path.isfile(fname)):
                    fp = open(fname, 'wb')
                    pickle.dump([request], fp)
                    fp.close()