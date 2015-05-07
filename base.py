import json
import sublime
import sublime_plugin
import threading
from elasticsearch import Elasticsearch

SETTINGS_FILE = 'Elasticsearch.sublime-settings'


def delete_ok_cancel_dialog(text):
    message = 'Are you sure you want to delete the {} ?'.format(text)
    return sublime.ok_cancel_dialog(message, ok_title='Delete')


class Settings(object):

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
    def backup_location(self):
        return self.settings.get('backup_location')

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
        sublime.save_settings(SETTINGS_FILE)


class ElasticsearchCommand(sublime_plugin.WindowCommand, Settings):
    show_result_on_window = True
    syntax = 'Packages/JavaScript/JSON.tmLanguage'
    result_window_title = ""

    def __init__(self, *args, **kwargs):
        self.settings = sublime.load_settings(SETTINGS_FILE)
        sublime_plugin.WindowCommand.__init__(self, *args, **kwargs)

    def request(self, method, *args, **kwargs):
        kwargs = kwargs or {}
        kwargs['command'] = self
        thread = threading.Thread(target=method, args=args, kwargs=kwargs)
        thread.start()

    def ESClient(self):
        return Elasticsearch(self.base_url, self.http_headers)

    def selection(self):
        view = self.window.active_view()
        sels = view.sel()
        if len(sels) == 1 and sels[0].empty():
            selection = view.substr(sublime.Region(0, view.size()))
            return selection

        selection = ''.join([view.substr(sel) for sel in sels])
        return selection

    def show_result_json(self, obj):

        text = json.dumps(obj, indent=4, ensure_ascii=False)
        self.show_result(text)
        return obj

    def show_result(self, text):
        if self.show_result_on_window:
            panel = self.window.new_file()
            panel.set_name('**{}**'.format(self.result_window_title))
            panel.set_scratch(True)
        else:
            panel = self.window.\
                create_output_panel('elasticsearch')
            self.window.run_command(
                "show_panel", {"panel": "output.elasticsearch"})

        panel.set_syntax_file(self.syntax)
        panel.set_scratch(True)
        panel.set_read_only(False)
        panel.settings().set('gutter', True)
        panel.settings().set('line_numbers', True)
        panel.settings().set('word_wrap', False)
        panel.run_command('append', {'characters': text})
        panel.set_read_only(True)
        return text


    def show_input_panel(self, label, default, callback):
        self.window.show_input_panel(label, default, callback, None, None)

    def get_index(self, callback):
        self.show_input_panel('Index: ', self.index, callback)

    def get_alias(self, callback):
        self.show_input_panel('Alias: ', '', callback)

    def get_fields(self, callback):
        self.show_input_panel('Comma-separated list of fields: ', '', callback)

    def get_field(self, callback):
        self.show_input_panel('Field: ', '*', callback)

    def get_node_id(self, callback):
        self.show_input_panel('Node ID: ', '', callback)

    def get_document_id(self, callback):
        self.show_input_panel('Document Id: ', '1', callback)

    def get_query(self, callback):
        self.show_input_panel('Query: ', '*', callback)

    def get_scroll_id(self, callback):
        self.show_input_panel('scroll_id: ', '', callback)

    def get_lang(self, callback):
        self.show_input_panel('Lang: ', 'groovy', callback)

    def get_script_id(self, callback):
        self.show_input_panel('Script Id: ', '', callback)

    def get_template_id(self, callback):
        self.show_input_panel('Template Id: ', '', callback)

    def get_analyzer(self, callback):
        self.show_input_panel('Analyzer: ', self.analyzer, callback)

    def get_include_feature(self, callback):
        self.show_input_panel(
            'Include features: ',
            '_settings,_mappings,_warmers,_aliases', callback)

    def get_index_template(self, callback):
        self.show_input_panel('Index Template: ', '', callback)

    def get_warmer(self, callback):
        self.show_input_panel('Index Warmer: ', '', callback)


class SwitchServersCommand(ElasticsearchCommand):
    selected_index = 0

    def run(self):
        self.select_panel(self.on_done)

    def select_panel(self, callback):
        self.server_choices = list(self.servers.keys())
        self.server_choices.sort()
        self.window.show_quick_panel(
            self.server_choices, self.on_done,
            selected_index=self.selected_index)

    def on_done(self, index):
        if index == -1:
            return
        self.selected_index = index
        selected = self.server_choices[index]
        self.settings.set('active_server', selected)
        self.save_settings()
        self.window.run_command('show_active_server')


class ShowActiveServerCommand(ElasticsearchCommand):
    show_result_on_window = False
    syntax = 'Packages/JavaScript/JSON.tmLanguage'

    def run(self):
        self.show_result_json({self.active_server: self.server_settings})
