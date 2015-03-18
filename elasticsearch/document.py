from .base import BaseElasticsearchCommand
from .base import make_path

__all__ = ["EsIndexDocumentCommand", "EsDeleteDocumentCommand",
           "EsGetDocumentCommand"]


class EsIndexDocumentCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsIndexDocumentCommand, self).run()

        if not self.enabled_index_document:
            self.status_message('*** Disabled Index Document! ***')
            return

        if not self.index:
            self.get_index(self.set_index)
            return

        if not self.doc_type:
            self.get_doc_type(self.set_doc_type)
            return

        self.get_doc_id(self.index_document)

    def set_index(self, index):
        super(EsIndexDocumentCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(EsIndexDocumentCommand, self).set_doc_type(doc_type)
        self.run()

    def index_document(self, doc_id):
        method = 'POST'
        url = make_path(self.index, self.doc_type)
        body = self.get_selection_text()
        if doc_id:
            method = 'PUT'
            url = make_path(self.index, self.doc_type, doc_id)
        self.run_request(method, url, body)


class EsDeleteDocumentCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsDeleteDocumentCommand, self).run()

        if not self.enabled_delete_document:
            self.status_message('*** Disabled Delete Document! ***')
            return

        if not self.index:
            self.get_index(self.set_index)
            return

        if not self.doc_type:
            self.get_doc_type(self.set_doc_type)
            return

        self.get_doc_id(self.delete_document)

    def set_index(self, index):
        super(EsDeleteDocumentCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(EsDeleteDocumentCommand, self).set_doc_type(doc_type)
        self.run()

    def delete_document(self, doc_id):
        if not doc_id:
            self.status_message('Canceled')
            return

        url = make_path(self.index, self.doc_type, doc_id)
        self.run_request('DELETE', url)


class EsGetDocumentCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsGetDocumentCommand, self).run()

        if not self.index:
            self.get_index(self.set_index)
            return

        if not self.doc_type:
            self.get_doc_type(self.set_doc_type)
            return

        self.get_doc_id(self.get_document)

    def set_index(self, index):
        super(EsGetDocumentCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(EsGetDocumentCommand, self).set_doc_type(doc_type)
        self.run()

    def get_document(self, doc_id):
        if not doc_id:
            self.status_message('Canceled')
            return

        url = make_path(self.index, self.doc_type, doc_id)
        self.run_request('GET', url)
