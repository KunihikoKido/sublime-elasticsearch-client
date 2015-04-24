"""
Base Modules for Elasticsearch Client for sublime text 3


"""

import threading
import tempfile
import json
import sublime
import sublime_plugin
from urllib.parse import urlencode
from .libs import requests

SETTINGS_FILE = 'Elasticsearch.sublime-settings'
SKIP_PATH = (None, '', b'', [], ())


def make_path(*parts):
    return '/'.join([p for p in parts if p not in SKIP_PATH])


def make_url(base_url, path, params={}):
    query_string = urlencode(params or {})
    url = ''.join([base_url, path])

    if query_string:
        return '{0}?{1}'.format(url, query_string)

    return url


def make_choices(choices):
    return [label for value, label in choices]


def choice(choices, index):
    return [value for value, label in choices][index]


class HttpRequestThread(threading.Thread):
    def __init__(self, method, url, **kwargs):
        threading.Thread.__init__(self)
        self.method = method
        self.url = url
        self.kwargs = kwargs
        self.result = None

    def run(self):
        try:
            self.result = requests.request(
                self.method.lower(), self.url, **self.kwargs)

        except requests.exceptions.Timeout as e:
            sublime.error_message('Error: Connection Timeout.')
            self.success = False
            return

        except requests.exceptions.RequestException as e:
            sublime.error_message("Error: {}".format(e))
            self.success = False
            return

        self.success = True


class ElasticsearchBaseCommand(sublime_plugin.WindowCommand):
    show_result_on_window = False
    syntax = 'Packages/JavaScript/JSON.tmLanguage'

    def __init__(self, *args, **kwargs):
        self.settings = sublime.load_settings(SETTINGS_FILE)
        sublime_plugin.WindowCommand.__init__(self, *args, **kwargs)

    @property
    def servers(self):
        return self.settings.get('servers')

    @property
    def active_server(self):
        active_server = self.settings.get('active_server', None)
        if active_server is None:
            active_server = list(self.servers.keys())[0]
        return active_server

    @property
    def server_settings(self):
        return self.servers[self.active_server]

    @property
    def ab_command(self):
        return self.settings.get('ab_command')

    @property
    def ab_options(self):
        return self.settings.get('ab_options', {})

    @property
    def benchmarks(self):
        return self.settings.get('benchmarks')

    @property
    def base_url(self):
        base_url = self.server_settings.get(
            'base_url', 'http://localhost:9200')
        if not base_url.endswith('/'):
            base_url += '/'
        return base_url

    @property
    def index(self):
        return self.server_settings.get('index', 'test')

    @property
    def doc_type(self):
        return self.server_settings.get('doc_type', 'test')

    @property
    def analyzer(self):
        return self.server_settings.get('analyzer', 'default')

    @property
    def http_headers(self):
        return self.server_settings.get('http_headers', {})

    def save_settings(self):
        sublime.save_settings('Elasticsearch.sublime-settings')

    def show_input_panel(self, label, default, callback):
        self.window.show_input_panel(label, default, callback, None, None)

    def show_result(self, text, title="** Elasticsearch Result **"):

        if not isinstance(text, str):
            text = json.dumps(text, indent=4, ensure_ascii=False)

        if self.show_result_on_window:
            panel = sublime.active_window().new_file()
            panel.set_name(title)
            panel.set_scratch(True)
        else:
            panel = sublime.active_window().\
                create_output_panel('elasticsearch')
            sublime.active_window().run_command(
                "show_panel", {"panel": "output.elasticsearch"})

        panel.set_read_only(False)
        panel.set_syntax_file(self.syntax)
        panel.settings().set('gutter', True)
        panel.settings().set('line_numbers', True)
        panel.settings().set('word_wrap', False)
        panel.run_command('append', {'characters': text})
        panel.set_read_only(True)

    def get_file_name(self):
        file_name = self.window.active_view().file_name()
        if not file_name:
            selection = self.get_selection()
            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.write(bytes(selection, 'utf-8'))
            file_name = temp.name
            temp.close()
        return file_name

    def get_selection(self):
        view = self.window.active_view()
        sels = view.sel()
        if len(sels) == 1 and sels[0].empty():
            selection = view.substr(sublime.Region(0, view.size()))
            return selection

        selection = ''.join([view.substr(sel) for sel in sels])
        return selection

    def status_message(self, message):
        sublime.status_message(message)

    def delete_ok_cancel_dialog(self, text):
        message = 'Are you sure you want to delete the {} ?'.format(text)
        return sublime.ok_cancel_dialog(message, ok_title='Delete')

    def get_index(self, callback):
        self.show_input_panel('Index: ', self.index, callback)

    def get_doc_type(self, callback):
        self.show_input_panel('Type: ', self.doc_type, callback)

    def get_document_id(self, callback):
        self.show_input_panel('Document Id: ', '', callback)

    def get_alias(self, callback):
        self.show_input_panel('Alias: ', '', callback)

    def get_analyzer(self, callback):
        self.show_input_panel('Analyzer: ', self.analyzer, callback)

    def get_warmer(self, callback):
        self.show_input_panel('Warmer Name: ', '', callback)

    def get_query(self, callback):
        self.show_input_panel('Query: ', '*', callback)

    def get_template(self, callback):
        self.show_input_panel('Template Name: ', '', callback)

    def update_server_settings(self, name, value):
        servers = self.servers
        servers[self.active_server][name] = value
        self.settings.set('servers', servers)
        self.save_settings()
        self.status_message('Changed {0}: {1}'.format(name, value))

    def set_index(self, index):
        if not index:
            return

        self.update_server_settings('index', index)

    def set_doc_type(self, doc_type):
        if not doc_type:
            return
        self.update_server_settings('doc_type', doc_type)


class HttpRequestCommand(ElasticsearchBaseCommand):

    def handle_thread(self, thread):
        if thread.is_alive():
            sublime.set_timeout(lambda: self.handle_thread(thread), 100)

        elif thread.success:
            self.complete_thread(thread)

    def complete_thread(self, thread):
        self.show_result(thread.result.json())

    def request(self, method, path, body=None, params={}):
        url = make_url(self.base_url, path, params)

        thread = HttpRequestThread(
            method, url, data=body, headers=self.http_headers)
        thread.start()

        self.handle_thread(thread)

    def request_get(self, path, body=None, params=None):
        return self.request('GET', path, body, params)

    def request_put(self, path, body=None, params=None):
        return self.request('PUT', path, body, params)

    def request_post(self, path, body=None, params=None):
        return self.request('POST', path, body, params)

    def request_delete(self, path, body=None, params=None):
        return self.request('DELETE', path, body, params)


class ReusltJsonCommand(HttpRequestCommand):
    syntax = 'Packages/JavaScript/JSON.tmLanguage'
    show_result_on_window = True
    result_window_title = "Elasticsearch"

    def complete_thread(self, thread):
        self.show_result(thread.result.json(), title=self.result_window_title)


class ReusltTextCommand(HttpRequestCommand):
    syntax = 'Packages/Text/Plain text.tmLanguage'
    show_result_on_window = True
    result_window_title = "Elasticsearch"

    def complete_thread(self, thread):
        self.show_result(thread.result.text, title=self.result_window_title)
