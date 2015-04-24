"""
Document API Commands for Elasticsearch Client for sublime text 3

For more information about API, see
http://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html
"""

from .elasticsearch import ReusltJsonCommand
from .elasticsearch import make_path
from .elasticsearch import DEFAULT_PARAMS


class ElasticsearchDeleteDocumentCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Delete Document **"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return

        if not self.delete_ok_cancel_dialog(
                '{} Document'.format(self.document_id)):
            return

        path = make_path(self.index, self.doc_type, document_id)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchGetDocumentCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Get Document **"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return

        path = make_path(self.index, self.doc_type, document_id)
        self.request_get(path, params=DEFAULT_PARAMS)


class ElasticsearchIndexDocumentCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Index Document **"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, document_id):
        path = make_path(self.index, self.doc_type, document_id)
        body = self.get_selection()
        if document_id:
            self.request_put(path, body=body, params=DEFAULT_PARAMS)
        else:
            self.request_post(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchUpdateDocumentCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Update Document **"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return
        path = make_path(self.index, self.doc_type, document_id, '_update')
        body = self.get_selection()
        self.request_post(path, body=body, params=DEFAULT_PARAMS)
