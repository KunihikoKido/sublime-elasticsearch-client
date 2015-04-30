from .base import ESClientBaseCommand


class UriSearchCommand(ESClientBaseCommand):
    result_window_title = "URI Search"

    def run(self, search_type='query_then_fetch'):
        self.get_query(self.on_done)

    def on_done(self, query):
        es = self.ESClient()
        params = dict(q=query)

        self.request(es.search, self.index, self.doc_type, params=params)


class RequestBodySearchCommand(ESClientBaseCommand):
    result_window_title = "Request Body Search"

    def run(self, search_type='query_then_fetch'):
        es = self.ESClient()
        params = dict(search_type=search_type)
        body = self.selection()

        self.request(es.search, self.index, self.doc_type,
                     body=body, params=params)


class SearchShardsCommand(ESClientBaseCommand):
    result_window_title = "Search Shards"

    def run(self):
        es = self.ESClient()
        self.request(es.search_shards, self.index, self.doc_type)


class SearchTemplateCommand(ESClientBaseCommand):
    result_window_title = "Search Template"

    def run(self, search_type='query_then_fetch'):
        es = self.ESClient()
        params = dict(search_type=search_type)
        body = self.selection()

        self.request(es.search_template, self.index, self.doc_type,
                     body=body, params=params)


class ExplainDocumentCommand(ESClientBaseCommand):
    result_window_title = "Explain Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if id is None:
            return

        es = self.ESClient()
        body = self.selection()

        self.request(es.explain, self.index, self.doc_type, id,
                     body=body)


class ScanCommand(ESClientBaseCommand):
    result_window_title = "Scan"

    def run(self):
        es = self.ESClient()
        params = dict(search_type='scan', scroll='5m')

        self.request(es.search, self.index,
                     self.doc_type, params=params)


class ScrollCommand(ESClientBaseCommand):
    result_window_title = "Scroll"

    def run(self):
        self.get_scroll_id(self.on_done)

    def on_done(self, scroll_id):
        if scroll_id == -1:
            return

        es = self.ESClient()
        params = dict(scroll='5m')

        self.request(es.scroll, scroll_id, params=params)


class ClearScrollCommand(ESClientBaseCommand):
    result_window_title = "Clear Scroll"

    def run(self):
        self.get_scroll_id(self.on_done)

    def on_done(self, scroll_id):
        if scroll_id == -1:
            return

        es = self.ESClient()

        self.request(es.clear_scroll, scroll_id)


class CountCommand(ESClientBaseCommand):
    result_window_title = "Count"

    def run(self):
        es = self.ESClient()
        body = self.selection()

        self.request(es.count, self.index, self.doc_type,
                     body=body, params=None)


class MultipleSearchCommand(ESClientBaseCommand):
    result_window_title = "Multiple Search"

    def run(self):
        es = self.ESClient()
        body = self.selection()

        self.request(es.msearch, body, self.index, self.doc_type)


class SuggestCommand(ESClientBaseCommand):
    result_window_title = "Suggest"

    def run(self):
        es = self.ESClient()
        body = self.selection()

        self.request(es.suggest, body, self.index)


class PercolateCommand(ESClientBaseCommand):
    result_window_title = "Percolate"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.percolate, self.index, self.doc_type,
                     body=body)


class MultiplePercolateCommand(ESClientBaseCommand):
    result_window_title = "Multiple Percolate"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.mpercolate, body, self.index, self.doc_type)


class CountPercolateCommmand(ESClientBaseCommand):
    result_window_title = "Count Percolate"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.count_percolate, self.index,
                     self.doc_type, body=body)


class MoreLikeThisCommand(ESClientBaseCommand):
    result_window_title = "More Like This"

    def run(self):
        self.get_document_id(self.on_done)

    def one_done(self, id):
        if not id:
            return

        es = self.ESClient()
        self.request(es.mlt, self.index, self.doc_type,
                     id)


class PutSearchTemplateCommand(ESClientBaseCommand):
    result_window_title = "Put Search Template"

    def run(self):
        self.get_template_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        es = self.ESClient()
        body = self.selection()
        self.request(es.put_template, id, body)


class GetSearchTemplateCommand(PutSearchTemplateCommand):
    result_window_title = "Get Search Template"

    def on_done(self, id):
        if not id:
            return

        es = self.ESClient()
        self.request(es.get_template, id)


class DeleteSearchTemplateCommand(PutSearchTemplateCommand):
    result_window_title = "Delete Search Template"

    def on_done(self, id):
        if not id:
            return

        es = self.ESClient()
        self.request(es.delete_template, id)


class SearchExistsCommand(ESClientBaseCommand):
    result_window_title = "Search Exists"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.search_exists, self.index, self.doc_type, body)


class ValidateQueryCommand(ESClientBaseCommand):
    result_window_title = "Validate Query"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(
            es.validate_query, self.index, self.doc_type, body)
