from .base import ElasticsearchCommand
from .base import delete_ok_cancel_dialog


class CreateDocumentCommand(ElasticsearchCommand):
    result_window_title = "Create Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        es = self.ESClient()
        body = self.selection()

        self.request(es.create, self.index, self.doc_type, body, id=id)


class IndexDocumentCommand(ElasticsearchCommand):
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


class GetDocumentCommand(ElasticsearchCommand):
    result_window_title = "Get Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        es = self.ESClient()
        self.request(es.get, self.index, self.doc_type, id)


class GetSourceCommand(ElasticsearchCommand):
    result_window_title = "Get Source"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        es = self.ESClient()
        self.request(es.get_source, self.index, self.doc_type, id)


class GetMultipleDocumentsCommand(ElasticsearchCommand):
    result_window_title = "Multi Get Doducments"

    def run(self):
        self.get_document_ids(self.on_done)

    def on_done(self, ids):
        if not ids:
            return

        ids = [id.strip() for id in ids.split(',') if id.strip()]

        es = self.ESClient()
        body = dict(ids=ids)
        self.request(es.mget, body, self.index, self.doc_type)


class UpdateDocumentCommand(ElasticsearchCommand):
    result_window_title = "Update Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        es = self.ESClient()
        body = self.selection()
        self.request(es.update, self.index, self.doc_type, id, body=body)


class DeleteDocumentCommand(ElasticsearchCommand):
    result_window_title = "Delete Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        if not delete_ok_cancel_dialog(id):
            return

        es = self.ESClient()
        self.request(es.delete, self.index, self.doc_type, id)


class DeletePercolaterCommand(DeleteDocumentCommand):
    result_window_title = "Delete Percolator"

    def on_done(self, id):
        if not id:
            return

        if not delete_ok_cancel_dialog(id):
            return

        es = self.ESClient()
        self.request(es.delete, self.index, '.percolator', id)


class BulkCommand(ElasticsearchCommand):
    result_window_title = "Bulk"

    def run(self):
        es = self.ESClient()
        body = self.selection()

        self.request(es.bulk, body, self.index, self.doc_type)


class DeleteByQueryCommand(ElasticsearchCommand):
    result_window_title = "Delete By Query"

    def run(self):
        if not delete_ok_cancel_dialog('Matched query documents'):
            return

        es = self.ESClient()
        body = self.selection()

        self.request(es.delete_by_query, self.index,
                     self.doc_type, body=body)


class TermvectorCommand(ElasticsearchCommand):
    result_window_title = "Termvector"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        es = self.ESClient()
        body = self.selection()
        self.request(es.termvector, self.index, self.doc_type, id, body=body)


class MultipleTermvectors(ElasticsearchCommand):
    result_window_title = "Multiple Termvectors"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.mtermvectors, self.index, self.doc_type, body=body)
