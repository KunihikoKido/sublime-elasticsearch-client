from .base import ESClientBaseCommand
from .base import delete_ok_cancel_dialog


class CreateDocumentCommand(ESClientBaseCommand):
    result_window_title = "Create Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        es = self.ESClient()
        body = self.selection()

        self.request(es.create, self.index, self.doc_type, body, id=id)


class IndexDocumentCommand(ESClientBaseCommand):
    result_window_title = "Index Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        es = self.ESClient()
        body = self.selection()

        self.request(es.index, self.index, self.doc_type, body, id=id)


class IndexPercolatorCommand(IndexDocumentCommand):
    result_window_title = "Index Percolator"

    def on_done(self, id):
        es = self.ESClient()
        body = self.selection()

        self.request(es.index, self.index, '.percolator', body, id=id)


class GetDocumentCommand(ESClientBaseCommand):
    result_window_title = "Get Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        es = self.ESClient()

        self.request(es.get, self.index, self.doc_type, id)


class GetSourceCommand(ESClientBaseCommand):
    result_window_title = "Get Source"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        es = self.ESClient()

        self.request(es.get_source, self.index, self.doc_type, id)


class GetMultipleDocumentsCommand(ESClientBaseCommand):
    result_window_title = "Multi Get Doducments"

    def run(self):
        es = self.ESClient()
        body = self.selection()

        self.request(es.mget, body, self.index, self.doc_type)


class UpdateDocumentCommand(ESClientBaseCommand):
    result_window_title = "Update Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        es = self.ESClient()
        body = self.selection()

        self.request(es.update, self.index, self.doc_type, id, body=body)


class DeleteDocumentCommand(ESClientBaseCommand):
    result_window_title = "Delete Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if id is None:
            return

        if not delete_ok_cancel_dialog(id):
            return

        es = self.ESClient()
        self.request(es.delete, self.index, self.doc_type, id)


class DeletePercolaterCommand(DeleteDocumentCommand):
    result_window_title = "Delete Percolator"

    def on_done(self, id):
        if id is None:
            return

        if not delete_ok_cancel_dialog(id):
            return

        es = self.ESClient()
        self.request(es.delete, self.index, '.percolator', id)


class BulkCommand(ESClientBaseCommand):
    result_window_title = "Bulk"

    def run(self):
        es = self.ESClient()
        body = self.selection()

        self.request(es.bulk, body, self.index, self.doc_type)


class DeleteByQueryCommand(ESClientBaseCommand):
    result_window_title = "Delete By Query"

    def run(self):
        if not delete_ok_cancel_dialog('Matched query documents'):
            return

        es = self.ESClient()
        body = self.selection()

        self.request(es.delete_by_query, self.index,
                     self.doc_type, body=body)


class TermvectorCommand(ESClientBaseCommand):
    result_window_title = "Termvector"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if id is None:
            return

        es = self.ESClient()
        body = self.selection()
        self.request(es.termvector, self.index, self.doc_type, id, body=body)


class MultipleTermvectors(ESClientBaseCommand):
    result_window_title = "Multiple Termvectors"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.mtermvectors, self.index, self.doc_type, body=body)

