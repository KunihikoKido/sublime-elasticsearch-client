"""
Search API Commands for Elasticsearch Client for sublime text 3

For more information about API, see
http://www.elastic.co/guide/en/elasticsearch/reference/current/search.html
"""

from .elasticsearch import ReusltJsonCommand
from .elasticsearch import make_path
from .elasticsearch import make_params
from .elasticsearch import make_choices
from .elasticsearch import choice
from .elasticsearch import DEFAULT_PARAMS

SEARCH_TYPE_CHOICES = (
    ('query_then_fetch', 'Search Type: Query Then Fetch (default)'),
    ('count', 'Search Type: Count'),
    ('dfs_query_and_fetch', 'Search Type: Dfs, Query And Fetch'),
    ('dfs_query_then_fetch', 'Search Type: Dfs, Query Then Fetch'),
    ('query_and_fetch', 'Search Type: Query And Fetch'),
)


class ElasticsearchSearchCommand(ReusltJsonCommand):

    selected_search_type = 0

    def run(self):
        if self.ask_to_search_types:
            self.select_panel(self.on_done)
        else:
            self.on_done(self.selected_search_type)

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
        params = make_params(search_type=search_type)
        body = self.get_selection()
        self.request_post(path, body=body, params=params)


class ElasticsearchTemplateSearchCommand(ElasticsearchSearchCommand):

    def on_done(self, index):
        if index == -1:
            return
        self.selected_search_type = index
        search_type = choice(SEARCH_TYPE_CHOICES, index)
        path = make_path(self.index, self.doc_type, '_search', 'template')
        params = make_params(search_type=search_type)
        body = self.get_selection()
        self.request_post(path, body=body, params=params)


class ElasticsearchUriSearchCommand(ReusltJsonCommand):

    def run(self):
        self.get_query(self.on_done)

    def on_done(self, query):
        path = make_path(self.index, self.doc_type, '_search')
        params = make_params(q=query)
        self.request_get(path, params=params)


class ElasticsearchBenchmarkCommand(ReusltJsonCommand):

    def run(self):
        path = make_path('_bench')
        body = self.get_selection()
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchDeletePercolatorCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_percolator():
            self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return
        path = make_path(self.index, '.percolator', document_id)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchExplainDocumentCommand(ReusltJsonCommand):

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return
        path = make_path(self.index, self.doc_type, document_id, '_explain')
        body = self.get_selection()
        self.request_post(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchMatchPercolatorCommand(ReusltJsonCommand):

    def run(self):
        path = make_path(self.index, self.doc_type, '_percolate')
        body = self.get_selection()
        self.request_post(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchRegisterPercolatorCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_register_query():
            self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return
        path = make_path(self.index, '.percolator', document_id)
        body = self.get_selection()
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchShowPercolatorCommand(ReusltJsonCommand):

    def run(self):
        path = make_path(self.index, '.percolator', '_search')
        self.request_get(path, params=DEFAULT_PARAMS)


class ElasticsearchValidateQueryCommand(ReusltJsonCommand):

    def run(self):
        path = make_path(self.index, self.doc_type, '_validate', 'query')
        body = self.get_selection()
        params = make_params(explain='true')
        self.request_post(path, body=body, params=params)


class ElasticsearchRegisterSearchTemplateCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_register_search_template():
            self.get_template(self.on_done)

    def on_done(self, template):
        if not template:
            return

        path = make_path('_search', 'template', template)
        body = self.get_selection()
        self.request_post(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchDeleteSearchTemplateCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_search_template():
            self.get_template(self.on_done)

    def on_done(self, template):
        if not template:
            return
        path = make_path('_search', 'template', template)
        self.request_delete(path, body=None, params=DEFAULT_PARAMS)


class ElasticsearchGetSearchTemplateCommand(ReusltJsonCommand):

    def run(self):
        self.get_template(self.on_done)

    def on_done(self, template):
        if template:
            path = make_path('_search', 'template', template)
            params = DEFAULT_PARAMS
        else:
            path = make_path('.scripts', '_search')
            params = make_params(_source='false')

        self.request_get(path, body=None, params=params)
