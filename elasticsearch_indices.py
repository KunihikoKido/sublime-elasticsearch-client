"""
Indices API Commands for Elasticsearch Client for sublime text 3

For more information about API, see
http://www.elastic.co/guide/en/elasticsearch/reference/current/indices.html
"""

from .elasticsearch import ReusltJsonCommand
from .elasticsearch import make_path
from .elasticsearch import make_params
from .elasticsearch import DEFAULT_PARAMS


class ElasticsearchAnalyzeCommand(ReusltJsonCommand):

    def run(self):
        self.get_analyzer(self.on_done)

    def on_done(self, analyzer):
        path = make_path(self.index, '_analyze')
        body = self.get_selection()
        params = make_params(analyzer=analyzer)
        self.request_post(path, body=body, params=params)


class ElasticsearchCreateIndexCommand(ReusltJsonCommand):

    def run(self, request_body=False):
        self.request_body = request_body
        if self.enabled_create_index():
            self.get_index(self.on_done)

    def on_done(self, index):
        if not index:
            return
        path = make_path(index)
        body = self.request_body and self.get_selection() or None
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchDeleteIndexCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_index():
            self.get_index(self.on_done)

    def on_done(self, index):
        if not index:
            return
        path = make_path(index)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchDeleteMappingCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_mapping():
            self.get_doc_type(self.on_done)

    def on_done(self, doc_type):
        if not doc_type:
            return
        path = make_path(self.index, doc_type)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchGetSettingsCommand(ReusltJsonCommand):

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        if not index:
            return
        path = make_path(index, '_settings')
        self.request_get(path, params=DEFAULT_PARAMS)


class ElasticsearchGetMappingCommand(ReusltJsonCommand):

    def run(self):
        self.get_doc_type(self.on_done)

    def on_done(self, doc_type):
        if not doc_type:
            return
        path = make_path(self.index, '_mapping', doc_type)
        self.request_get(path, params=DEFAULT_PARAMS)


class ElasticsearchPutMappingCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_put_mapping():
            self.get_doc_type(self.on_done)

    def on_done(self, doc_type):
        if not doc_type:
            return
        path = make_path(self.index, '_mapping', doc_type)
        body = self.get_selection()
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchPutWarmerCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_put_warmer():
            self.get_warmer(self.on_done)

    def on_done(self, name):
        if not name:
            return
        path = make_path(self.index, '_warmer', name)
        body = self.get_selection()
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchDeleteWarmerCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_warmer():
            self.get_warmer(self.on_done)

    def on_done(self, name):
        if not name:
            return
        path = make_path(self.index, '_warmer', name)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchGetWarmerCommand(ReusltJsonCommand):

    def run(self):
        self.get_warmer(self.on_done)

    def on_done(self, name):
        path = make_path(self.index, '_warmer', name)
        self.request_get(path, params=DEFAULT_PARAMS)


class ElasticsearchAddAliasCommand(ReusltJsonCommand):

    def run(self, request_body=False):
        self.request_body = request_body
        if self.enabled_add_alias():
            self.get_alias(self.on_done)

    def on_done(self, alias):
        path = make_path(self.index, '_alias', alias)
        body = self.request_body and self.get_selection() or None
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchDeleteAliasCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_alias():
            self.get_alias(self.on_done)

    def on_done(self, alias):
        path = make_path(self.index, '_alias', alias)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchGetAliasCommand(ReusltJsonCommand):

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, alias):
        path = make_path(self.index, '_alias', alias)
        self.request_get(path, params=DEFAULT_PARAMS)
