from elasticsearch import Urllib3HttpConnection


class CustomHeadersConnection(Urllib3HttpConnection):
    def __init__(self, host='localhost', port=80, headers=None, **kwargs):
        super(CustomHeadersConnection, self).__init__(host=host, port=port, **kwargs)
        if headers is not None:
            self.headers.update(headers)
