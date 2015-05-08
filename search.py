from .base import ElasticsearchCommand


class UriSearchCommand(ElasticsearchCommand):
    result_window_title = "URI Search"

    def run(self, search_type='query_then_fetch'):
        self.get_query(self.on_done)

    def on_done(self, query):
        params = dict(q=query)
        self.request(self.esclient.search,
                     self.index, self.doc_type, params=params)


class RequestBodySearchCommand(ElasticsearchCommand):
    result_window_title = "Request Body Search"

    def run(self, search_type='query_then_fetch'):
        params = dict(search_type=search_type)
        body = self.selection()
        self.request(self.esclient.search,
                     self.index, self.doc_type, body=body, params=params)


class SearchShardsCommand(ElasticsearchCommand):
    result_window_title = "Search Shards"

    def run(self):
        self.request(self.esclient.search_shards, self.index, self.doc_type)


class SearchTemplateCommand(ElasticsearchCommand):
    result_window_title = "Search Template"

    def run(self, search_type='query_then_fetch'):
        params = dict(search_type=search_type)
        body = self.selection()
        self.request(self.esclient.search_template, self.index, self.doc_type,
                     body=body, params=params)


class ExplainDocumentCommand(ElasticsearchCommand):
    result_window_title = "Explain Document"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        if id is None:
            return

        body = self.selection()
        self.request(self.esclient.explain,
                     self.index, self.doc_type, id, body=body)


class ScanCommand(ElasticsearchCommand):
    result_window_title = "Scan"

    def run(self):
        params = dict(search_type='scan', scroll='5m')
        self.request(self.esclient.search,
                     self.index, self.doc_type, params=params)


class ScrollCommand(ElasticsearchCommand):
    result_window_title = "Scroll"

    def run(self):
        self.get_scroll_id(self.on_done)

    def on_done(self, scroll_id):
        if scroll_id == -1:
            return

        params = dict(scroll='5m')
        self.request(self.esclient.scroll, scroll_id, params=params)


class ClearScrollCommand(ElasticsearchCommand):
    result_window_title = "Clear Scroll"

    def run(self):
        self.get_scroll_id(self.on_done)

    def on_done(self, scroll_id):
        if scroll_id == -1:
            return

        self.request(self.esclient.clear_scroll, scroll_id)


class CountCommand(ElasticsearchCommand):
    result_window_title = "Count"

    def run(self):
        body = self.selection()
        self.request(self.esclient.count,
                     self.index, self.doc_type, body=body, params=None)


class MultipleSearchCommand(ElasticsearchCommand):
    result_window_title = "Multiple Search"

    def run(self):
        body = self.selection()
        self.request(self.esclient.msearch, body, self.index, self.doc_type)


class SuggestCommand(ElasticsearchCommand):
    result_window_title = "Suggest"

    def run(self):
        body = self.selection()
        self.request(self.esclient.suggest, body, self.index)


class PercolateCommand(ElasticsearchCommand):
    result_window_title = "Percolate"

    def run(self):
        body = self.selection()
        self.request(self.esclient.percolate,
                     self.index, self.doc_type, body=body)


class MultiplePercolateCommand(ElasticsearchCommand):
    result_window_title = "Multiple Percolate"

    def run(self):
        body = self.selection()
        self.request(self.esclient.mpercolate, body, self.index, self.doc_type)


class CountPercolateCommmand(ElasticsearchCommand):
    result_window_title = "Count Percolate"

    def run(self):

        body = self.selection()
        self.request(self.esclient.count_percolate,
                     self.index, self.doc_type, body=body)


class MoreLikeThisCommand(ElasticsearchCommand):
    result_window_title = "More Like This"

    def run(self):
        self.get_document_id(self.on_done)

    def one_done(self, id):
        if not id:
            return

        self.request(self.esclient.mlt, self.index, self.doc_type, id)


class PutSearchTemplateCommand(ElasticsearchCommand):
    result_window_title = "Put Search Template"

    def run(self):
        self.get_template_id(self.on_done)

    def on_done(self, id):
        if not id:
            return

        body = self.selection()
        self.request(self.esclient.put_template, id, body)


class GetSearchTemplateCommand(PutSearchTemplateCommand):
    result_window_title = "Get Search Template"

    def on_done(self, id):
        if not id:
            return

        self.request(self.esclient.get_template, id)


class DeleteSearchTemplateCommand(PutSearchTemplateCommand):
    result_window_title = "Delete Search Template"

    def on_done(self, id):
        if not id:
            return

        self.request(self.esclient.delete_template, id)


class SearchExistsCommand(ElasticsearchCommand):
    result_window_title = "Search Exists"

    def run(self):

        body = self.selection()
        self.request(self.esclient.search_exists,
                     self.index, self.doc_type, body)


class ValidateQueryCommand(ElasticsearchCommand):
    result_window_title = "Validate Query"

    def run(self):

        body = self.selection()
        self.request(self.esclient.validate_query,
                     self.index, self.doc_type, body)
