from .base import ElasticsearchCommand
from .base import delete_ok_cancel_dialog


class CreateDocumentCommand(ElasticsearchCommand):
    result_window_title = "Create Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        body = self.selection()
        self.request(self.esclient.create,
                     self.index, self.doc_type, body, id=id)


class IndexDocumentCommand(ElasticsearchCommand):
    result_window_title = "Index Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        body = self.selection()
        self.request(self.esclient.index,
                     self.index, self.doc_type, body, id=id)


class IndexPercolatorCommand(IndexDocumentCommand):
    result_window_title = "Index Percolator"

    def on_done(self, id):
        body = self.selection()
        self.request(self.esclient.index,
                     self.index, '.percolator', body, id=id)


class GetDocumentCommand(ElasticsearchCommand):
    result_window_title = "Get Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        self.request(self.esclient.get,
                     self.index, self.doc_type, id)


class GetSourceCommand(ElasticsearchCommand):
    result_window_title = "Get Source"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        self.request(self.esclient.get_source, self.index, self.doc_type, id)


class GetMultipleDocumentsCommand(ElasticsearchCommand):
    result_window_title = "Multi Get Doducments"

    def run(self):
        self.get_document_ids(self.on_done)

    def on_done(self, ids):
        if not ids:
            return

        ids = [id.strip() for id in ids.split(',') if id.strip()]
        body = dict(ids=ids)
        self.request(self.esclient.mget, body, self.index, self.doc_type)


class UpdateDocumentCommand(ElasticsearchCommand):
    result_window_title = "Update Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        body = self.selection()
        self.request(self.esclient.update,
                     self.index, self.doc_type, id, body=body)


class DeleteDocumentCommand(ElasticsearchCommand):
    result_window_title = "Delete Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        if not delete_ok_cancel_dialog(id):
            return

        self.request(self.esclient.delete, self.index, self.doc_type, id)


class DeletePercolaterCommand(DeleteDocumentCommand):
    result_window_title = "Delete Percolator"

    def on_done(self, id):
        if not id:
            return

        if not delete_ok_cancel_dialog(id):
            return

        self.request(self.esclient.delete, self.index, '.percolator', id)


class BulkCommand(ElasticsearchCommand):
    result_window_title = "Bulk"

    def run(self):

        body = self.selection()

        self.request(self.esclient.bulk, body, self.index, self.doc_type)


class DeleteByQueryCommand(ElasticsearchCommand):
    result_window_title = "Delete By Query"

    def run(self):
        if not delete_ok_cancel_dialog('Matched query documents'):
            return

        body = self.selection()
        self.request(self.esclient.delete_by_query, self.index,
                     self.doc_type, body=body)


class TermvectorCommand(ElasticsearchCommand):
    result_window_title = "Termvector"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        body = self.selection()
        self.request(self.esclient.termvector,
                     self.index, self.doc_type, id, body=body)


class MultipleTermvectors(ElasticsearchCommand):
    result_window_title = "Multiple Termvectors"

    def run(self):
        body = self.selection()
        self.request(self.esclient.mtermvectors,
                     self.index, self.doc_type, body=body)
