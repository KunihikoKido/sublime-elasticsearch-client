"""
Indices API Commands for Elasticsearch Client for sublime text 3

For more information about API, see
http://www.elastic.co/guide/en/elasticsearch/reference/current/indices.html
"""
from .elasticsearch import ReusltJsonCommand
from .elasticsearch import make_path


class ElasticsearchAnalyzeCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Analyze **"

    def run(self):
        self.get_analyzer(self.on_done)

    def on_done(self, analyzer):
        path = make_path(self.index, '_analyze')
        body = self.get_selection()
        params = dict(analyzer=analyzer)
        self.request_post(path, body=body, params=params)


class ElasticsearchCreateIndexCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Create Index **"

    def run(self, request_body=False):
        self.request_body = request_body
        path = make_path(self.index)
        body = self.request_body and self.get_selection() or None
        self.request_put(path, body=body)


class ElasticsearchDeleteIndexCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Delete Index **"

    def run(self):
        if not self.delete_ok_cancel_dialog(
                '{} Index'.format(self.index)):
            return

        path = make_path(self.index)
        self.request_delete(path)


class ElasticsearchDeleteMappingCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Delete Mapping **"

    def run(self):
        if not self.delete_ok_cancel_dialog(
                '{} Mapping'.format(self.doc_type)):
            return

        path = make_path(self.index, self.doc_type)
        self.request_delete(path)


class ElasticsearchGetSettingsCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Get Index Settings **"

    def run(self):
        path = make_path(self.index, '_settings')
        self.request_get(path)


class ElasticsearchGetMappingCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Get Mapping **"

    def run(self):
        path = make_path(self.index, '_mapping', self.doc_type)
        self.request_get(path)


class ElasticsearchPutMappingCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Put Mapping **"

    def run(self):
        path = make_path(self.index, '_mapping', self.doc_type)
        body = self.get_selection()
        self.request_put(path, body=body)


class ElasticsearchPutWarmerCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Put Warmer **"

    def run(self):
        self.get_warmer(self.on_done)

    def on_done(self, name):
        if not name:
            return
        path = make_path(self.index, '_warmer', name)
        body = self.get_selection()
        self.request_put(path, body=body)


class ElasticsearchDeleteWarmerCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Delete Warmer **"

    def run(self):
        self.get_warmer(self.on_done)

    def on_done(self, warmer):
        if not warmer:
            return

        if not self.delete_ok_cancel_dialog(
                '{} Warmer'.format(self.warmer)):
            return

        path = make_path(self.index, '_warmer', warmer)
        self.request_delete(path)


class ElasticsearchGetWarmerCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Get Warmer **"

    def run(self):
        self.get_warmer(self.on_done)

    def on_done(self, name):
        path = make_path(self.index, '_warmer', name)
        self.request_get(path)


class ElasticsearchAddAliasCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Add Alias **"

    def run(self, request_body=False):
        self.request_body = request_body
        self.get_alias(self.on_done)

    def on_done(self, alias):
        path = make_path(self.index, '_alias', alias)
        body = self.request_body and self.get_selection() or None
        self.request_put(path, body=body)


class ElasticsearchDeleteAliasCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Delete Alias **"

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, alias):
        if not alias:
            return

        if not self.delete_ok_cancel_dialog(
                '{} Alias'.format(self.alias)):
            return

        path = make_path(self.index, '_alias', alias)
        self.request_delete(path)


class ElasticsearchGetAliasCommand(ReusltJsonCommand):
    result_window_title = "** Elasticsearch: Get Alias **"

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, alias):
        path = make_path(self.index, '_alias', alias)
        self.request_get(path)
