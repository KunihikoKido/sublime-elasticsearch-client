"""
Search API Commands for Elasticsearch Client for sublime text 3

For more information about API, see
http://www.elastic.co/guide/en/elasticsearch/reference/current/search.html
"""

from .elasticsearch import ReusltJsonCommand
from .elasticsearch import make_path
from .elasticsearch import make_choices
from .elasticsearch import choice

SEARCH_TYPE_CHOICES = (
    ('query_then_fetch', 'Search Type: Query Then Fetch (default)'),
    ('count', 'Search Type: Count'),
    ('dfs_query_and_fetch', 'Search Type: Dfs, Query And Fetch'),
    ('dfs_query_then_fetch', 'Search Type: Dfs, Query Then Fetch'),
    ('query_and_fetch', 'Search Type: Query And Fetch'),
)


class ElasticsearchSearchCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Search Result **"

    selected_search_type = 0

    def run(self):
        self.select_panel(self.on_done)

    def select_panel(self, callback):
        choices = make_choices(SEARCH_TYPE_CHOICES)
        self.window.show_quick_panel(
            choices, callback, selected_index=self.selected_search_type)

    def on_done(self, index):
        if index == -1:
            return
        self.selected_search_type = index
        search_type = choice(SEARCH_TYPE_CHOICES, index)
        path = make_path(self.index, self.doc_type, '_search')
        params = dict(search_type=search_type)
        body = self.get_selection()
        self.request_post(path, body=body, params=params)


class ElasticsearchTemplateSearchCommand(ElasticsearchSearchCommand):
    result_window_title = "** Elasticsearch: Search Result **"

    def on_done(self, index):
        if index == -1:
            return
        self.selected_search_type = index
        search_type = choice(SEARCH_TYPE_CHOICES, index)
        path = make_path(self.index, self.doc_type, '_search', 'template')
        params = dict(search_type=search_type)
        body = self.get_selection()
        self.request_post(path, body=body, params=params)


class ElasticsearchUriSearchCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Search Result **"

    def run(self):
        self.get_query(self.on_done)

    def on_done(self, query):
        path = make_path(self.index, self.doc_type, '_search')
        params = dict(q=query)
        self.request_get(path, params=params)


class ElasticsearchBenchmarkCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Benchmark **"

    def run(self):
        path = make_path('_bench')
        body = self.get_selection()
        self.request_put(path, body=body)


class ElasticsearchDeletePercolatorCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Delete Percolator **"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return

        if not self.delete_ok_cancel_dialog(
                '{} Percolator'.format(self.document_id)):
            return

        path = make_path(self.index, '.percolator', document_id)
        self.request_delete(path)


class ElasticsearchExplainDocumentCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Explain Document **"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return
        path = make_path(self.index, self.doc_type, document_id, '_explain')
        body = self.get_selection()
        self.request_post(path, body=body)


class ElasticsearchMatchPercolatorCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Match Percolator **"

    def run(self):
        path = make_path(self.index, self.doc_type, '_percolate')
        body = self.get_selection()
        self.request_post(path, body=body)


class ElasticsearchRegisterPercolatorCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Register Percolator **"

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return
        path = make_path(self.index, '.percolator', document_id)
        body = self.get_selection()
        self.request_put(path, body=body)


class ElasticsearchShowPercolatorCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Show Percolator **"

    def run(self):
        path = make_path(self.index, '.percolator', '_search')
        self.request_get(path)


class ElasticsearchValidateQueryCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Validate Query **"

    def run(self):
        path = make_path(self.index, self.doc_type, '_validate', 'query')
        body = self.get_selection()
        params = dict(explain='true')
        self.request_post(path, body=body, params=params)


class ElasticsearchRegisterSearchTemplateCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Register Search Template **"

    def run(self):
        self.get_template(self.on_done)

    def on_done(self, template):
        if not template:
            return

        path = make_path('_search', 'template', template)
        body = self.get_selection()
        self.request_post(path, body=body)


class ElasticsearchDeleteSearchTemplateCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Delete Search Template **"

    def run(self):
        self.get_template(self.on_done)

    def on_done(self, template):
        if not template:
            return

        if not self.delete_ok_cancel_dialog(
                '{} Search Template'.format(self.template)):
            return

        path = make_path('_search', 'template', template)
        self.request_delete(path, body=None)


class ElasticsearchGetSearchTemplateCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Get Search Template **"

    def run(self):
        self.get_template(self.on_done)

    def on_done(self, template):
        if template:
            path = make_path('_search', 'template', template)
            params = None
        else:
            path = make_path('.scripts', '_search')
            params = dict(_source='false')

        self.request_get(path, body=None, params=params)
