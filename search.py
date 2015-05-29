from .base import ElasticsearchCommand
from .base import delete_ok_cancel_dialog


class UriSearchCommand(ElasticsearchCommand):
    result_window_title = "URI Search"

    def run(self, search_type='query_then_fetch'):
        self.search_type = search_type
        self.get_query(self.on_done)

    def on_done(self, query):
        self.request_api(
            'search', index=self.index, doc_type=self.doc_type,
            params=dict(q=query, search_type=self.search_type))


class RequestBodySearchCommand(ElasticsearchCommand):
    result_window_title = "Request Body Search"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self, search_type='query_then_fetch'):
        self.request_api(
            'search', index=self.index, doc_type=self.doc_type,
            body=self.selection(), params=dict(search_type=search_type))


class SearchShardsCommand(ElasticsearchCommand):
    result_window_title = "Search Shards"

    def run(self):
        self.request_api(
            'search_shards', index=self.index, doc_type=self.doc_type)


class SearchTemplateCommand(ElasticsearchCommand):
    result_window_title = "Search Template"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self, search_type='query_then_fetch'):
        self.request_api(
            'search_template', index=self.index, doc_type=self.doc_type,
            body=self.selection(), params=dict(search_type=search_type))


class ExplainDocumentCommand(ElasticsearchCommand):
    result_window_title = "Explain Document"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, id):
        self.request_api(
            'explain', index=self.index, doc_type=self.doc_type,
            id=id, body=self.selection())


class ScanCommand(ElasticsearchCommand):
    result_window_title = "Scan"

    def run(self):
        self.request_api(
            'search', index=self.index, doc_type=self.doc_type,
            params=dict(search_type='scan', scroll='5m'))


class ScrollCommand(ElasticsearchCommand):
    result_window_title = "Scroll"

    def run(self):
        self.get_scroll_id(self.on_done)

    def on_done(self, scroll_id):
        self.request_api(
            'scroll', scroll_id=scroll_id, params=dict(scroll='5m'))


class ClearScrollCommand(ElasticsearchCommand):
    show_result_on_window = False
    result_window_title = "Clear Scroll"

    def run(self):
        self.get_scroll_id(self.on_done)

    def on_done(self, scroll_id):
        self.request_api('clear_scroll', scroll_id=scroll_id)


class CountCommand(ElasticsearchCommand):
    result_window_title = "Count"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_api(
            'count', index=self.index, doc_type=self.doc_type,
            body=self.selection())


class MultipleSearchCommand(ElasticsearchCommand):
    result_window_title = "Multiple Search"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_api(
            'msearch', index=self.index, doc_type=self.doc_type,
            body=self.selection())


class SuggestCommand(ElasticsearchCommand):
    result_window_title = "Suggest"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_api('suggest', index=self.index, body=self.selection())


class PercolateCommand(ElasticsearchCommand):
    result_window_title = "Percolate"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_api(
            'percolate', index=self.index, doc_type=self.doc_type,
            body=self.selection())


class MultiplePercolateCommand(ElasticsearchCommand):
    result_window_title = "Multiple Percolate"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_api(
            'mpercolate', index=self.index, doc_type=self.doc_type,
            body=self.selection())


class CountPercolateCommmand(ElasticsearchCommand):
    result_window_title = "Count Percolate"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_api(
            'count_percolate', index=self.index, doc_type=self.doc_type,
            body=self.selection())


class MoreLikeThisCommand(ElasticsearchCommand):
    result_window_title = "More Like This"

    def run(self):
        self.get_document_id(self.on_done)

    def one_done(self, id):
        self.request_api(
            'mlt', index=self.index, doc_type=self.doc_type, id=id)


class PutSearchTemplateCommand(ElasticsearchCommand):
    show_result_on_window = False
    result_window_title = "Put Search Template"

    def is_enabled(self):
        if self.selection():
            return True
        return False

    def run(self):
        self.get_template_id(self.on_done)

    def on_done(self, id):
        self.request_api('put_template', id=id, body=self.selection())


class GetSearchTemplateCommand(PutSearchTemplateCommand):
    result_window_title = "Get Search Template"

    def on_done(self, id):
        self.request_api('get_template', id=id)


class DeleteSearchTemplateCommand(PutSearchTemplateCommand):
    show_result_on_window = False
    result_window_title = "Delete Search Template"

    def on_done(self, id):
        if not delete_ok_cancel_dialog(id):
            return

        self.request_api('delete_template', id=id)


class SearchExistsCommand(ElasticsearchCommand):
    result_window_title = "Search Exists"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_api(
            'search_exists', index=self.index, doc_type=self.doc_type,
            body=self.selection())


class ValidateQueryCommand(ElasticsearchCommand):
    result_window_title = "Validate Query"

    def is_enabled(self):
        return self.is_valid_json()

    def run(self):
        self.request_api(
            'validate_query', index=self.index, doc_type=self.doc_type,
            body=self.selection(), params=dict(explain=1))
