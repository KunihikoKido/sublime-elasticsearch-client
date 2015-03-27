"""
Document API Commands for Elasticsearch Client for sublime text 3

For more information about API, see
http://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html
"""

from .elasticsearch import ReusltJsonCommand
from .elasticsearch import make_path
from .elasticsearch import DEFAULT_PARAMS


class ElasticsearchDeleteDocumentCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_document():
            self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return
        path = make_path(self.index, self.doc_type, document_id)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchGetDocumentCommand(ReusltJsonCommand):

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return

        path = make_path(self.index, self.doc_type, document_id)
        self.request_get(path, params=DEFAULT_PARAMS)


class ElasticsearchIndexDocumentCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_index_document():
            self.get_document_id(self.on_done)

    def on_done(self, document_id):
        path = make_path(self.index, self.doc_type, document_id)
        body = self.get_selection()
        if document_id:
            self.request_put(path, body=body, params=DEFAULT_PARAMS)
        else:
            self.request_post(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchUpdateDocumentCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_update_document():
            self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return
        path = make_path(self.index, self.doc_type, document_id, '_update')
        body = self.get_selection()
        self.request_post(path, body=body, params=DEFAULT_PARAMS)
