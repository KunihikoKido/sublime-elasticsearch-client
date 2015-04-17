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
        if not self.enabled_create_index():
            return

        self.request_body = request_body
        path = make_path(self.index)
        body = self.request_body and self.get_selection() or None
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchDeleteIndexCommand(ReusltJsonCommand):

    def run(self):
        if not self.enabled_delete_index():
            return

        if not self.delete_ok_cancel_dialog(
                '{} Index'.format(self.index)):
            return

        path = make_path(self.index)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchDeleteMappingCommand(ReusltJsonCommand):

    def run(self):
        if not self.enabled_delete_mapping():
            return

        if not self.delete_ok_cancel_dialog(
                '{} Mapping'.format(self.doc_type)):
            return

        path = make_path(self.index, self.doc_type)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchGetSettingsCommand(ReusltJsonCommand):

    def run(self):
        path = make_path(self.index, '_settings')
        self.request_get(path, params=DEFAULT_PARAMS)


class ElasticsearchGetMappingCommand(ReusltJsonCommand):

    def run(self):
        path = make_path(self.index, '_mapping', self.doc_type)
        self.request_get(path, params=DEFAULT_PARAMS)


class ElasticsearchPutMappingCommand(ReusltJsonCommand):

    def run(self):
        if not self.enabled_put_mapping():
            return

        path = make_path(self.index, '_mapping', self.doc_type)
        body = self.get_selection()
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchPutWarmerCommand(ReusltJsonCommand):

    def run(self):
        if not self.enabled_put_warmer():
            return

        self.get_warmer(self.on_done)

    def on_done(self, name):
        if not name:
            return
        path = make_path(self.index, '_warmer', name)
        body = self.get_selection()
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchDeleteWarmerCommand(ReusltJsonCommand):

    def run(self):
        if not self.enabled_delete_warmer():
            return

        self.get_warmer(self.on_done)

    def on_done(self, warmer):
        if not warmer:
            return

        if not self.delete_ok_cancel_dialog(
                '{} Warmer'.format(self.warmer)):
            return

        path = make_path(self.index, '_warmer', warmer)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchGetWarmerCommand(ReusltJsonCommand):

    def run(self):
        self.get_warmer(self.on_done)

    def on_done(self, name):
        path = make_path(self.index, '_warmer', name)
        self.request_get(path, params=DEFAULT_PARAMS)


class ElasticsearchAddAliasCommand(ReusltJsonCommand):

    def run(self, request_body=False):
        if not self.enabled_add_alias():
            return

        self.request_body = request_body
        self.get_alias(self.on_done)

    def on_done(self, alias):
        path = make_path(self.index, '_alias', alias)
        body = self.request_body and self.get_selection() or None
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchDeleteAliasCommand(ReusltJsonCommand):

    def run(self):
        if not self.enabled_delete_alias():
            return

        self.get_alias(self.on_done)

    def on_done(self, alias):
        if not alias:
            return

        if not self.delete_ok_cancel_dialog(
                '{} Alias'.format(self.alias)):
            return

        path = make_path(self.index, '_alias', alias)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchGetAliasCommand(ReusltJsonCommand):

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, alias):
        path = make_path(self.index, '_alias', alias)
        self.request_get(path, params=DEFAULT_PARAMS)
