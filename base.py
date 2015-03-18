# -*- coding: utf-8 -*-
import tempfile
from urllib.parse import urlencode
import sublime
import sublime_plugin

DEFAULT_PARAMS = {'pretty': 'true'}
SKIP_PATH = (None, '', b'', [], ())


def make_path(*parts):
    return '/'.join([p for p in parts if p not in SKIP_PATH])


class BaseElasticsearchCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.settings = sublime.load_settings('Elasticsearch.sublime-settings')
        self.curl_command = self.settings.get('curl_command')
        self.ab_command = self.settings.get('ab_command')
        self.servers = self.settings.get('servers')
        self.active_server = self.settings.get("active_server")
        self.benchmarks = self.settings.get('benchmarks')
        self.quiet = self.settings.get('quiet', True)

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
        params = urlencode(params or DEFAULT_PARAMS)
        if url:
            return '{0}{1}?{2}'.format(self.base_url, url, params)
        return '{0}?{1}'.format(self.base_url, params)

    def run_request(self, method, url=None, body=None, params=None):
        curl_command = [self.curl_command, '-s', '-X', method]
        request_url = self.get_request_url(url, params)
        curl_command += [request_url]

        if body:
            curl_command += ['-d', body]

        for k, v in self.http_headers.items():
            curl_command += ['-H', "{0}: {1}".format(k, v)]

        self.window.run_command(
            'exec', {'cmd': curl_command, 'quiet': self.quiet})

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
        self.save_settings()
        self.status_message('Changed index: {0}'.format(index_name))

    def set_doc_type(self, doc_type):
        if not doc_type:
            return  # canceled
        self.servers[self.active_server]['doc_type'] = doc_type
        self.settings.set('servers', self.servers)
        self.save_settings()
        self.status_message('Changed Type: {0}'.format(doc_type))

    def set_analyzer(self, analyzer):
        if not analyzer:
            return  # canceled
        self.servers[self.active_server]['analyzer'] = analyzer
        self.settings.set('servers', self.servers)
        self.save_settings()
        self.status_message('Changed Type: {0}'.format(analyzer))

    def save_settings(self):
        sublime.save_settings('Elasticsearch.sublime-settings')

    def get_index(self, callback):
        self.window.show_input_panel(
            'Index: ', self.index, callback, None, None)

    def get_doc_type(self, callback):
        self.window.show_input_panel(
            'Document Type: ', self.doc_type, callback, None, None)

    def get_doc_id(self, callback):
        self.window.show_input_panel(
            'Document Id: ', '', callback, None, None)

    def get_analyzer(self, callback):
        self.window.show_input_panel(
            'Analyzer: ', self.analyzer, callback, None, None)

    def status_message(self, message):
        sublime.status_message(message)

    def panel(self, text):
        output_panel = self.window.get_output_panel("textarea")
        output_panel.set_syntax_file('')
        self.window.run_command("show_panel", {"panel": "output.textarea"})
        output_panel.run_command("insert", {"characters": text})

    @property
    def filename(self):
        filename = self.window.active_view().file_name()
        if not filename:
            text = self.get_selection_text()
            tmp = tempfile.NamedTemporaryFile(delete=False)
            tmp.write(bytes(text, 'utf-8'))
            filename = tmp.name
            tmp.close()
        return filename
