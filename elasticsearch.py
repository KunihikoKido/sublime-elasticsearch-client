"""
Base Modules for Elasticsearch Client for sublime text 3


"""

import tempfile
from urllib.parse import urlencode
import sublime
import sublime_plugin

SETTINGS_FILE = 'Elasticsearch.sublime-settings'
DEFAULT_PARAMS = {'pretty': 'true'}
SKIP_PATH = (None, '', b'', [], ())


def make_path(*parts):
    return '/'.join([p for p in parts if p not in SKIP_PATH])


def make_choices(choices):
    return [label for value, label in choices]


def choice(choices, index):
    return [value for value, label in choices][index]


def make_params(**options):
    params = DEFAULT_PARAMS.copy()
    params.update(dict(options))
    return params


class BaseCommand(sublime_plugin.WindowCommand):

    def __init__(self, *args, **kwargs):
        self.settings = sublime.load_settings(SETTINGS_FILE)
        sublime_plugin.WindowCommand.__init__(self, *args, **kwargs)

    def active_view(self):
        return self.window.active_view()

    def run_command(self, command):
        self.window.run_command('exec', {'cmd': command, 'quiet': self.quiet})

        output_panel = self.window.get_output_panel('exec')
        output_panel.set_syntax_file(self.syntax)
        output_panel.settings().set('gutter', True)
        output_panel.settings().set('line_numbers', True)
        output_panel.settings().set('wrap_width', 0)
        self.window.run_command(
            'show_panel', {'panel': 'output.exec'})

    def show_input_panel(self, label, default, callback):
        self.window.show_input_panel(label, default, callback, None, None)

    def show_output_panel(self, output):
        output_panel = self.window.get_output_panel('elasticsearch')
        output_panel.set_read_only(False)
        output_panel.set_syntax_file(self.syntax)
        output_panel.settings().set("auto_indent", False)
        output_panel.run_command('append', {'characters': output})
        output_panel.set_read_only(True)
        self.window.run_command(
            'show_panel', {'panel': 'output.elasticsearch'})

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

    def save_settings(self):
        sublime.save_settings('Elasticsearch.sublime-settings')

    def status_message(self, message):
        sublime.status_message(message)


class ElasticsearchBaseCommand(BaseCommand):

    @property
    def servers(self):
        return self.settings.get('servers')

    @property
    def active_server(self):
        return self.settings.get('active_server')

    @property
    def server_settings(self):
        active_server = self.active_server
        if self.active_server is None:
            active_server = list(self.servers.keys())[0]
        return self.servers[active_server]

    @property
    def curl_command(self):
        return self.settings.get('curl_command')

    @property
    def ab_command(self):
        return self.settings.get('ab_command')

    @property
    def quiet(self):
        return self.settings.get('quiet', True)

    @property
    def ask_to_search_types(self):
        return self.settings.get('ask_to_search_types', False)

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

    def command_status_message(self, enabled, quiet=False):
        if not enabled and quiet is False:
            sublime.message_dialog(
                'Disabled This Command!\n\n'
                'Change the settings: '
                'Preferences > Package Settings > '
                'ElasticsearchClient > Settings – User menu'
            )
        return enabled

    def enabled_create_index(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_create_index', False),
            quiet)

    def enabled_put_mapping(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_put_mapping', False),
            quiet)

    def enabled_delete_document(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_delete_document', False),
            quiet)

    def enabled_delete_index(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_delete_index', False),
            quiet)

    def enabled_delete_mapping(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_delete_mapping', False),
            quiet)

    def enabled_index_document(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_index_document', False),
            quiet)

    def enabled_update_document(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_update_document', False),
            quiet)

    def enabled_register_query(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_register_query', False),
            quiet)

    def enabled_delete_percolator(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_delete_percolator', False),
            quiet)

    def enabled_put_warmer(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_put_warmer', False),
            quiet)

    def enabled_delete_warmer(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_delete_warmer', False),
            quiet)

    def enabled_add_alias(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_add_alias', False),
            quiet)

    def enabled_delete_alias(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_delete_alias', False),
            quiet)

    def enabled_register_search_template(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_register_search_template', False),
            quiet)

    def enabled_delete_search_template(self, quiet=False):
        return self.command_status_message(
            self.server_settings.get('enabled_delete_search_template', False),
            quiet)

    @property
    def http_headers(self):
        return self.server_settings.get('http_headers', {})

    def get_request_url(self, path, params=None):
        params = urlencode(params or {})
        url = ''.join([self.base_url, path])
        return '{0}?{1}'.format(url, params)

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
        self.show_input_panel('Query: ', '', callback)

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

    def run_request(self, method, path, body=None, params=None):
        url = self.get_request_url(path, params)

        command = [self.curl_command, '-s',
                   '-X', method, '-d', body or '', url]

        for k, v in self.http_headers.items():
            command += ['-H', "{0}: {1}".format(k, v)]

        self.run_command(command)

    def request_get(self, path, body=None, params=None):
        return self.run_request('GET', path, body, params)

    def request_put(self, path, body=None, params=None):
        return self.run_request('PUT', path, body, params)

    def request_post(self, path, body=None, params=None):
        return self.run_request('POST', path, body, params)

    def request_delete(self, path, body=None, params=None):
        return self.run_request('DELETE', path, body, params)

    def show_active_server_settings(self):
        self.show_output_panel(
            "# =============================================================\n"
            "# Active Server Settings [{active_server}]\n"
            "# =============================================================\n"
            "\n[ Base Settings ]\n"
            "- base_url                          : '{base_url}'\n"
            "- index                             : '{index}'\n"
            "- doc_type                          : '{doc_type}'\n"
            "- analyzer                          : '{analyzer}'\n"
            "\n[ Indices APIs ]\n"
            "- enabled_add_alias                 : {enabled_add_alias}\n"
            "- enabled_create_index              : {enabled_create_index}\n"
            "- enabled_delete_alias              : {enabled_delete_alias}\n"
            "- enabled_delete_index              : {enabled_delete_index}\n"
            "- enabled_delete_mapping            : {enabled_delete_mapping}\n"
            "- enabled_delete_warmer             : {enabled_delete_warmer}\n"
            "- enabled_put_mapping               : {enabled_put_mapping}\n"
            "- enabled_put_warmer                : {enabled_put_warmer}\n"
            "\n[ Document APIs ]\n"
            "- enabled_delete_document           : {enabled_delete_document}\n"
            "- enabled_index_document            : {enabled_index_document}\n"
            "- enabled_update_document           : {enabled_update_document}\n"
            "\n[ Search APIs ]\n"
            "- enabled_delete_percolator         : {enabled_delete_percolator}\n"
            "- enabled_register_query            : {enabled_register_query}\n"
            "- enabled_register_search_template  : {enabled_register_search_template}\n"
            "- enabled_delete_search_template    : {enabled_delete_search_template}\n"
            "".format(
                active_server=self.active_server,
                base_url=self.base_url,
                index=self.index,
                doc_type=self.doc_type,
                analyzer=self.analyzer,
                enabled_create_index=self.enabled_create_index(quiet=True),
                enabled_delete_document=self.enabled_delete_document(quiet=True),
                enabled_delete_index=self.enabled_delete_index(quiet=True),
                enabled_delete_mapping=self.enabled_delete_mapping(quiet=True),
                enabled_delete_percolator=self.enabled_delete_percolator(quiet=True),
                enabled_index_document=self.enabled_index_document(quiet=True),
                enabled_put_mapping=self.enabled_put_mapping(quiet=True),
                enabled_register_query=self.enabled_register_query(quiet=True),
                enabled_put_warmer=self.enabled_put_warmer(quiet=True),
                enabled_delete_warmer=self.enabled_delete_warmer(quiet=True),
                enabled_add_alias=self.enabled_add_alias(quiet=True),
                enabled_delete_alias=self.enabled_delete_alias(quiet=True),
                enabled_update_document=self.enabled_update_document(quiet=True),
                enabled_register_search_template=self.enabled_register_search_template(quiet=True),
                enabled_delete_search_template=self.enabled_delete_search_template(quiet=True)
            )
        )


class ReusltJsonCommand(ElasticsearchBaseCommand):
    syntax = 'Packages/JavaScript/JSON.tmLanguage'


class ReusltTextCommand(ElasticsearchBaseCommand):
    syntax = 'Packages/Text/Plain text.tmLanguage'
