from .base import ElasticsearchCommand
from .base import delete_ok_cancel_dialog


class CreateDocumentCommand(ElasticsearchCommand):
    show_result_on_window = False
    result_window_title = "Create Document"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        self.request_api(
            'create', index=self.index, doc_type=self.doc_type,
            body=self.selection(), id=id)


class IndexDocumentCommand(ElasticsearchCommand):
    show_result_on_window = False
    result_window_title = "Index Document"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        self.request_api(
            'index', index=self.index, doc_type=self.doc_type,
            body=self.selection(), id=id)


class IndexPercolatorCommand(IndexDocumentCommand):
    show_result_on_window = False
    result_window_title = "Index Percolator"

    def is_enabled(self):
        return self.is_valid_json()

    def on_done(self, id):
        self.request_api(
            'index', index=self.index, doc_type='.percolator',
            body=self.selection(), id=id)


class GetDocumentCommand(ElasticsearchCommand):
    result_window_title = "Get Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        self.request_api(
            'get', index=self.index, doc_type=self.doc_type, id=id)


class GetSourceCommand(ElasticsearchCommand):
    result_window_title = "Get Source"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        self.request_api(
            'get_source', index=self.index, doc_type=self.doc_type, id=id)


class GetMultipleDocumentsCommand(ElasticsearchCommand):
    result_window_title = "Multi Get Doducments"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.get_document_ids(self.on_done)

    def make_body(self, ids):
        ids = [id.strip() for id in ids.split(',') if id.strip()]
        return dict(ids=ids)

    def on_done(self, ids):
        self.request_api(
            'mget', index=self.index, doc_type=self.doc_type,
            body=self.make_body(ids))


class UpdateDocumentCommand(ElasticsearchCommand):
    show_result_on_window = False
    result_window_title = "Update Document"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        self.request_api(
            'update', index=self.index, doc_type=self.doc_type,
            id=id, body=self.selection())


class DeleteDocumentCommand(ElasticsearchCommand):
    show_result_on_window = False
    result_window_title = "Delete Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if not delete_ok_cancel_dialog(id):
            return

        self.request_api(
            'delete', index=self.index, doc_type=self.doc_type, id=id)


class DeletePercolaterCommand(DeleteDocumentCommand):
    show_result_on_window = False
    result_window_title = "Delete Percolator"

    def on_done(self, id):
        if not delete_ok_cancel_dialog(id):
            return

        self.request_api(
            'delete', index=self.index, doc_type='.percolator', id=id)


class BulkCommand(ElasticsearchCommand):
    show_result_on_window = False
    result_window_title = "Bulk"

    def is_enabled(self):
        if self.selection():
            return True
        return False

    def run(self):
        self.request_api(
            'bulk', index=self.index, doc_type=self.doc_type,
            body=self.selection())


class DeleteByQueryCommand(ElasticsearchCommand):
    show_result_on_window = False
    result_window_title = "Delete By Query"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        if not delete_ok_cancel_dialog('Matched query documents'):
            return

        self.request_api(
            'delete_by_query', index=self.index,
            doc_type=self.doc_type, body=self.selection())


class TermvectorCommand(ElasticsearchCommand):
    result_window_title = "Termvector"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        self.request_api(
            'termvector', index=self.index, doc_type=self.doc_type,
            id=id, body=self.selection())


class MultipleTermvectors(ElasticsearchCommand):
    result_window_title = "Multiple Termvectors"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_api(
            'mtermvectors', index=self.index, doc_type=self.doc_type,
            body=self.selection())
