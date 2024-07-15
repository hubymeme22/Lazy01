class SimpleHTTPRequestParser:
    def __init__(self, request: str) -> None:
        self.request = request
        self.errorFlag = None
        self.method = ''
        self.host = ''
        self.path = ''
        self.header = {}

        try:
            # filter to separate body from data
            requestDetails = request.replace('\r', '').split('\n\n')
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