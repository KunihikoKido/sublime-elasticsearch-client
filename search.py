from .base import make_path
from .base import BaseElasticsearchCommand


class EsSearchRequestCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsSearchRequestCommand, self).run()
        url = make_path(self.index, self.doc_type, '_search')
        body = self.get_selection_text()
        self.run_request('POST', url, body)


class EsRegisterPercolatorCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsRegisterPercolatorCommand, self).run()

        if not self.enabled_register_query:
            self.status_message(
                '*** Disabled Register Query (Percolator)! ***')
            return

        if not self.index:
            self.get_index(self.set_index)

        self.get_doc_id(self.register_query)

    def set_index(self, index):
        super(EsRegisterPercolatorCommand, self).set_index(index)
        self.run()

    def register_query(self, doc_id):
        if not doc_id:
            self.status_message('Canceled')
            return

        url = make_path(self.index, '.percolator', doc_id)
        body = self.get_selection_text()
        self.run_request('PUT', url, body)


class EsShowPercolatorCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsShowPercolatorCommand, self).run()

        if not self.index:
            self.get_index(self.set_index)
            return

        url = make_path(self.index, '.percolator', '_search')
        self.run_request('POST', url)

    def set_index(self, index):
        super(EsShowPercolatorCommand, self).set_index(index)
        self.run()


class EsMatchPercolatorCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsMatchPercolatorCommand, self).run()

        if not self.index:
            self.get_index(self.set_index)
            return

        if not self.doc_type:
            self.get_doc_type(self.set_doc_type)
            return

        url = make_path(self.index, self.doc_type, '_percolate')
        body = self.get_selection_text()
        self.run_request('POST', url, body)

    def set_index(self, index):
        super(EsMatchPercolatorCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(EsMatchPercolatorCommand, self).set_doc_type(doc_type)
        self.run()


class EsDeletePercolatorCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsDeletePercolatorCommand, self).run()

        if not self.enabled_delete_percolator:
            self.status_message('*** Disabled Delete Percolator! ***')
            return

        if not self.index:
            self.get_index(self.set_index)
            return

        if not self.doc_type:
            self.get_doc_type(self.set_doc_type)
            return

        self.get_doc_id(self.delete_percolator)

    def set_index(self, index):
        super(EsDeletePercolatorCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(EsDeletePercolatorCommand, self).set_doc_type(doc_type)
        self.run()

    def delete_percolator(self, doc_id):
        if not doc_id:
            self.status_message('Canceled')
            return

        url = make_path(self.index, '.percolator', doc_id)
        self.run_request('DELETE', url)


class EsBenchmarkCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsBenchmarkCommand, self).run()
        url = make_path('_bench')
        body = self.get_selection_text()
        self.run_request('PUT', url, body)


class EsExplainDocumentCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsExplainDocumentCommand, self).run()

        if not self.index:
            self.get_index(self.set_index)
            return

        if not self.doc_type:
            self.get_doc_type(self.set_doc_type)
            return

        self.get_doc_id(self.get_document)

    def set_index(self, index):
        super(EsExplainDocumentCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(EsExplainDocumentCommand, self).set_doc_type(doc_type)
        self.run()

    def get_document(self, doc_id):
        if not doc_id:
            self.status_message('Canceled')
            return

        body = self.get_selection_text()
        url = make_path(self.index, self.doc_type, doc_id, '_explain')
        self.run_request('POST', url, body)
