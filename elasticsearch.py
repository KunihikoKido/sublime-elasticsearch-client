# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import sublime
import sublime_plugin


SKIP_PATH = (None, '', b'', [], ())


def make_path(*parts):
    return '/'.join([p for p in parts if p not in SKIP_PATH])


class BaseElasticsearchCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.settings = sublime.load_settings('Elasticsearch.sublime-settings')
        self.servers = self.settings.get('servers')
        self.active_server = self.settings.get("active_server")
        if not self.active_server:
            self.active_server = list(self.servers.keys())[0]

        server_settings = self.servers[self.active_server]

        self.base_url = server_settings.get(
            'base_url', 'http://localhost:9200/')
        if not self.base_url.endswith('/'):
            self.base_url += '/'
        self.index = server_settings.get('index', 'test')
        self.doc_type = server_settings.get('doc_type', 'test')
        self.http_headers = server_settings.get('http_headers', {})

        self.analyzer = server_settings.get('analyzer', 'default')
        self.enabled_create_index = server_settings.get(
            'enabled_create_index', False)
        self.enabled_put_mapping = server_settings.get(
            'enabled_put_mapping', False)
        self.enabled_delete_document = server_settings.get(
            'enabled_delete_document', False)
        self.enabled_delete_index = server_settings.get(
            'enabled_delete_index', False)
        self.enabled_delete_mapping = server_settings.get(
            'enabled_delete_mapping', False)
        self.enabled_index_document = server_settings.get(
            'enabled_index_document', False)
        self.enabled_register_query = server_settings.get(
            'enabled_register_query', False)
        self.enabled_delete_percolator = server_settings.get(
            'enabled_delete_percolator', False)

    def get_request_url(self, url, params):
        params = urlencode(params or {})
        if url:
            return '{0}{1}?{2}'.format(self.base_url, url, params)
        return '{0}?{1}'.format(self.base_url, params)

    def curl_request(self, method, url=None, body=None, params=None):
        curl_command = ['curl', '-s', '-X', method]
        request_url = self.get_request_url(url, params)
        curl_command += [request_url]

        if body:
            curl_command += ['-d', body]

        for k, v in self.http_headers.items():
            curl_command += ['-H', "{0}: {1}".format(k, v)]

        self.window.run_command('exec', {'cmd': curl_command, 'quiet': True})

    def get_selection_text(self):
        view = self.window.active_view()
        sels = view.sel()
        if len(sels) == 1 and sels[0].empty():
            text = view.substr(sublime.Region(0, view.size()))
            return text
        text = ''.join([view.substr(sel) for sel in sels])
        return text

    def set_index(self, index_name):
        if not index_name:
            return  # canceled
        self.servers[self.active_server]['index'] = index_name
        self.settings.set('servers', self.servers)
        sublime.save_settings("Elasticsearch.sublime-settings")
        sublime.status_message('Changed index: {0}'.format(index_name))

    def set_doc_type(self, doc_type):
        if not doc_type:
            return  # canceled
        self.servers[self.active_server]['doc_type'] = doc_type
        self.settings.set('servers', self.servers)
        sublime.save_settings("Elasticsearch.sublime-settings")
        sublime.status_message('Changed Type: {0}'.format(doc_type))

    def set_analyzer(self, analyzer):
        if not analyzer:
            return  # canceled
        self.servers[self.active_server]['analyzer'] = analyzer
        self.settings.set('servers', self.servers)
        sublime.save_settings("Elasticsearch.sublime-settings")
        sublime.status_message('Changed Type: {0}'.format(analyzer))


class ElasticsearchSearchRequestCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchSearchRequestCommand, self).run()

        body = self.get_selection_text()
        self.curl_request(
            'POST',
            make_path(self.index, self.doc_type, '_search'), body,
            {'pretty': 'true'})


class ElasticsearchCreateIndexCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchCreateIndexCommand, self).run()

        if not self.enabled_create_index:
            sublime.status_message('*** Disabled Create Index! ***')
            return

        self.window.show_input_panel(
            'Index: ', self.index, self.create_index, None, None)

    def create_index(self, index):
        if not index:
            sublime.status_message('Canceled')
            return

        self.curl_request(
            'PUT', make_path(self.index), None, {'pretty': 'true'})

        self.set_index(index)


class ElasticsearchPutMappingCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchPutMappingCommand, self).run()

        if not self.enabled_put_mapping:
            sublime.status_message('*** Disabled Put Mapping! ***')
            return

        if not self.index:
            self.window.show_input_panel(
                'Index: ', '', self.set_index, None, None)
            return

        self.window.show_input_panel(
            '({0}) Doc Type: '.format(self.index),
            self.doc_type, self.put_mapping, None, None)

    def set_index(self, index):
        super(ElasticsearchPutMappingCommand, self).set_index(index)
        self.run()

    def put_mapping(self, doc_type):
        if not doc_type:
            sublime.status_message('Canceled')
            return

        body = self.get_selection_text()
        self.curl_request(
            'PUT', make_path(self.index, '_mapping', doc_type),
            body, {'pretty': 'true'})

        self.set_doc_type(doc_type)


class ElasticsearchAnalyzeCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchAnalyzeCommand, self).run()

        if not self.index:
            self.window.show_input_panel(
                'Index: ', '', self.set_index, None, None)
            return

        self.window.show_input_panel(
            '({0}) Analyzer: '.format(self.index),
            self.analyzer, self.analyze, None, None)

    def set_index(self, index):
        super(ElasticsearchAnalyzeCommand, self).set_index(index)
        self.run()

    def analyze(self, analyzer):
        if not analyzer:
            sublime.status_message('canceled')
            return

        body = self.get_selection_text()
        self.curl_request(
            'POST', make_path(self.index, '_analyze'), body,
            {'pretty': 'true', 'analyzer': analyzer})

        self.set_analyzer(analyzer)


class ElasticsearchClusterHealthCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchClusterHealthCommand, self).run()

        self.curl_request(
            'GET', make_path('_cat', 'health'), None, {'v': 'true'})


class ElasticsearchListAllIndexesCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchListAllIndexesCommand, self).run()

        self.curl_request(
            'GET', make_path('_cat', 'indices'), None, {'v': 'true'})


class ElasticsearchGetIndexSettingsCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchGetIndexSettingsCommand, self).run()

        self.window.show_input_panel(
            'Index: ', self.index, self.get_index_settings, None, None)
        return

    def get_index_settings(self, index):
        if not index:
            sublime.status_message('Canceled')
            return

        self.curl_request(
            'GET', make_path(index, '_settings'),
            None, {'pretty': 'true'})

        self.set_index(index)


class ElasticsearchGetMappingCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchGetMappingCommand, self).run()

        if not self.index:
            self.window.show_input_panel(
                'Index: ', '', self.set_index, None, None)
            return

        self.window.show_input_panel(
            '({0}) Doc Type: '.format(self.index),
            self.doc_type, self.get_mapping, None, None)

    def set_index(self, index):
        super(ElasticsearchGetMappingCommand, self).set_index(index)
        self.run()

    def get_mapping(self, doc_type):
        if not doc_type:
            sublime.status_message('Canceled')
            return

        self.curl_request(
            'GET', make_path(self.index, '_mapping', doc_type),
            None, {'pretty': 'true'})

        self.set_doc_type(doc_type)


class ElasticsearchIndexDocumentCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchIndexDocumentCommand, self).run()

        if not self.enabled_index_document:
            sublime.status_message('*** Disabled Index Document! ***')
            return

        if not self.index:
            self.window.show_input_panel(
                'Index: ', '', self.set_index, None, None)
            return

        if not self.doc_type:
            self.window.show_input_panel(
                '({0}) Doc Type: '.format(self.index),
                '', self.set_doc_type, None, None)
            return

        self.window.show_input_panel(
            '({0}/{1}) Document ID: '.format(self.index, self.doc_type),
            '', self.index_document, None, None)

    def set_index(self, index):
        super(ElasticsearchIndexDocumentCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(ElasticsearchIndexDocumentCommand, self).set_doc_type(doc_type)
        self.run()

    def index_document(self, doc_id):
        body = self.get_selection_text()
        if doc_id:
            self.curl_request(
                'PUT', make_path(self.index, self.doc_type, doc_id),
                body, {'pretty': 'true'})
            return

        self.curl_request(
            'POST', make_path(self.index, self.doc_type),
            body, {'pretty': 'true'})


class ElasticsearchDeleteDocumentCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchDeleteDocumentCommand, self).run()

        if not self.enabled_delete_document:
            sublime.status_message('*** Disabled Delete Document! ***')
            return

        if not self.index:
            self.window.show_input_panel(
                'Index: ', '', self.set_index, None, None)
            return

        if not self.doc_type:
            self.window.show_input_panel(
                '({0}) Doc Type: '.format(self.index),
                '', self.set_doc_type, None, None)
            return

        self.window.show_input_panel(
            '({0}/{1}) Document ID: '.format(self.index, self.doc_type),
            '', self.delete_document, None, None)

    def set_index(self, index):
        super(ElasticsearchDeleteDocumentCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(ElasticsearchDeleteDocumentCommand, self).set_doc_type(doc_type)
        self.run()

    def delete_document(self, doc_id):
        if not doc_id:
            sublime.status_message('Canceled')
            return

        self.curl_request(
            'DELETE', make_path(self.index, self.doc_type, doc_id),
            None, {'pretty': 'true'})


class ElasticsearchGetDocumentCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchGetDocumentCommand, self).run()

        if not self.index:
            self.window.show_input_panel(
                'Index: ', '', self.set_index, None, None)
            return

        if not self.doc_type:
            self.window.show_input_panel(
                '({0}) Doc Type: '.format(self.index),
                '', self.set_doc_type, None, None)
            return

        self.window.show_input_panel(
            '({0}/{1}) Document ID: '.format(self.index, self.doc_type),
            '', self.get_document, None, None)

    def set_index(self, index):
        super(ElasticsearchGetDocumentCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(ElasticsearchGetDocumentCommand, self).set_doc_type(doc_type)
        self.run()

    def get_document(self, doc_id):
        if not doc_id:
            sublime.status_message('Canceled')
            return

        self.curl_request(
            'GET', make_path(self.index, self.doc_type, doc_id),
            None, {'pretty': 'true'})


class ElasticsearchDeleteIndexCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchDeleteIndexCommand, self).run()

        if not self.enabled_delete_index:
            sublime.status_message('*** Disabled Delete Index! ***')
            return

        self.window.show_input_panel(
            'Index: ', self.index, self.delete_index, None, None)

    def delete_index(self, index):
        if not index:
            sublime.status_message('Canceled')
            return

        self.curl_request('DELETE', make_path(index), None, {'pretty': 'true'})


class ElasticsearchDeleteMappingCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchDeleteMappingCommand, self).run()

        if not self.enabled_delete_mapping:
            sublime.status_message('*** Disabled Delete Mapping! ***')
            return

        if not self.index:
            self.window.show_input_panel(
                'Index: ', '', self.set_index, None, None)
            return

        self.window.show_input_panel(
            '({0}) Doc Type: '.format(self.index),
            self.doc_type, self.delete_mapping, None, None)

    def set_index(self, index):
        super(ElasticsearchDeleteMappingCommand, self).set_index(index)
        self.run()

    def delete_mapping(self, doc_type):
        if not doc_type:
            sublime.status_message('Canceled')
            return

        self.curl_request(
            'DELETE', make_path(self.index, doc_type),
            None, {'pretty': 'true'})

        self.set_doc_type(doc_type)


class ElasticsearchRegisterPercolatorCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchRegisterPercolatorCommand, self).run()

        if not self.enabled_register_query:
            sublime.status_message(
                '*** Disabled Register Query (Percolator)! ***')
            return

        if not self.index:
            self.window.show_input_panel(
                'Index: ', self.index, self.set_index, None, None)

        self.window.show_input_panel(
            '({0}) Percolator ID : '.format(self.index),
            '', self.register_query, None, None)

    def set_index(self, index):
        super(ElasticsearchRegisterPercolatorCommand, self).set_index(index)
        self.run()

    def register_query(self, percolator_id):
        if not percolator_id:
            sublime.status_message('Canceled')
            return

        body = self.get_selection_text()
        self.curl_request(
            'PUT', make_path(self.index, '.percolator', percolator_id),
            body, {'pretty': 'true'})


class ElasticsearchShowPercolatorCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchShowPercolatorCommand, self).run()

        if not self.index:
            self.window.show_input_panel(
                'Index: ', '', self.set_index, None, None)
            return

        self.curl_request(
            'POST', make_path(self.index, '.percolator', '_search'),
            None, {'pretty': 'true'})

    def set_index(self, index):
        super(ElasticsearchIndexDocumentCommand, self).set_index(index)
        self.run()


class ElasticsearchMatchPercolatorCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchMatchPercolatorCommand, self).run()

        if not self.index:
            self.window.show_input_panel(
                'Index: ', '', self.set_index, None, None)
            return

        if not self.doc_type:
            self.window.show_input_panel(
                '({0}) Doc Type: '.format(self.index),
                '', self.set_doc_type, None, None)
            return

        body = self.get_selection_text()
        self.curl_request(
            'POST', make_path(self.index, self.doc_type, '_percolate'),
            body, {'pretty': 'true'})

    def set_index(self, index):
        super(ElasticsearchIndexDocumentCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(ElasticsearchIndexDocumentCommand, self).set_doc_type(doc_type)
        self.run()


class ElasticsearchDeletePercolatorCommand(BaseElasticsearchCommand):

    def run(self):
        super(ElasticsearchDeletePercolatorCommand, self).run()

        if not self.enabled_delete_percolator:
            sublime.status_message('*** Disabled Delete Percolator! ***')
            return

        if not self.index:
            self.window.show_input_panel(
                'Index: ', '', self.set_index, None, None)
            return

        if not self.doc_type:
            self.window.show_input_panel(
                '({0}) Doc Type: '.format(self.index),
                '', self.set_doc_type, None, None)
            return

        self.window.show_input_panel(
            '({0}) Percolator ID: '.format(self.index),
            '', self.delete_percolator, None, None)

    def set_index(self, index):
        super(ElasticsearchDeletePercolatorCommand, self).set_index(index)
        self.run()

    def set_doc_type(self, doc_type):
        super(ElasticsearchDeletePercolatorCommand, self).\
            set_doc_type(doc_type)
        self.run()

    def delete_percolator(self, percolator_id):
        if not percolator_id:
            sublime.status_message('Canceled')
            return

        self.curl_request(
            'DELETE', make_path(self.index, '.percolator', percolator_id),
            None, {'pretty': 'true'})


class SwitchServersCommand(BaseElasticsearchCommand):

    def run(self):
        super(SwitchServersCommand, self).run()
        servers = list(self.servers.keys())
        self.window.show_quick_panel(servers, self.server_selected)

    def server_selected(self, index):
        if index == -1:
            sublime.status_message('Canceled')
            return  # canceled
        self.active_server = list(self.servers.keys())[index]
        self.settings.set("active_server", self.active_server)
        sublime.save_settings("Elasticsearch.sublime-settings")


class ShowActiveServerCommand(BaseElasticsearchCommand):

    def run(self):
        super(ShowActiveServerCommand, self).run()
        sublime.status_message(
            'Elasticsearch: {0} ({1} / {2})'.format(
                self.active_server, self.index, self.doc_type))


class ChangeIndexCommand(BaseElasticsearchCommand):

    def run(self):
        super(ChangeIndexCommand, self).run()
        self.window.show_input_panel(
            'Change to: ', self.index, self.set_index, None, None)


class ChangeDocTypeCommand(BaseElasticsearchCommand):

    def run(self):
        super(ChangeDocTypeCommand, self).run()
        self.window.show_input_panel(
            '({0}) Change to: '.format(self.index),
            self.doc_type, self.set_doc_type, None, None)
