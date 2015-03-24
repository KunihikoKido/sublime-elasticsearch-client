import tempfile
from urllib.parse import urlencode
import sublime
import sublime_plugin

SETTINGS_FILE = 'Elasticsearch.sublime-settings'
DEFAULT_PARAMS = {'pretty': 'true'}
SKIP_PATH = (None, '', b'', [], ())


def make_path(*parts):
    return '/'.join([p for p in parts if p not in SKIP_PATH])


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
        return self.servers[self.active_server]

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

    @property
    def enabled_create_index(self):
        return self.server_settings.get('enabled_create_index', False)

    @property
    def enabled_put_mapping(self):
        return self.server_settings.get('enabled_put_mapping', False)

    @property
    def enabled_delete_document(self):
        return self.server_settings.get('enabled_delete_document', False)

    @property
    def enabled_delete_index(self):
        return self.server_settings.get('enabled_delete_index', False)

    @property
    def enabled_delete_mapping(self):
        return self.server_settings.get('enabled_delete_mapping', False)

    @property
    def enabled_index_document(self):
        return self.server_settings.get('enabled_index_document', False)

    @property
    def enabled_register_query(self):
        return self.server_settings.get('enabled_register_query', False)

    @property
    def enabled_delete_percolator(self):
        return self.server_settings.get('enabled_delete_percolator', False)

    @property
    def enabled_put_warmer(self):
        return self.server_settings.get('enabled_put_warmer', False)

    @property
    def enabled_delete_warmer(self):
        return self.server_settings.get('enabled_delete_warmer', False)

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
            "- base_url                     : '{base_url}'\n"
            "- index                        : '{index}'\n"
            "- doc_type                     : '{doc_type}'\n"
            "- analyzer                     : '{analyzer}'\n"
            "- enabled_create_index         : {enabled_create_index}\n"
            "- enabled_delete_document      : {enabled_delete_document}\n"
            "- enabled_delete_index         : {enabled_delete_index}\n"
            "- enabled_delete_mapping       : {enabled_delete_mapping}\n"
            "- enabled_delete_percolator    : {enabled_delete_percolator}\n"
            "- enabled_index_document       : {enabled_index_document}\n"
            "- enabled_put_mapping          : {enabled_put_mapping}\n"
            "- enabled_register_query       : {enabled_register_query}\n"
            "".format(
                active_server=self.active_server,
                base_url=self.base_url,
                index=self.index,
                doc_type=self.doc_type,
                analyzer=self.analyzer,
                enabled_create_index=self.enabled_create_index,
                enabled_delete_document=self.enabled_delete_document,
                enabled_delete_index=self.enabled_delete_index,
                enabled_delete_mapping=self.enabled_delete_mapping,
                enabled_delete_percolator=self.enabled_delete_percolator,
                enabled_index_document=self.enabled_index_document,
                enabled_put_mapping=self.enabled_put_mapping,
                enabled_register_query=self.enabled_register_query
            )
        )


class ReusltJsonCommand(ElasticsearchBaseCommand):
    syntax = 'Packages/JavaScript/JSON.tmLanguage'


class ReusltTextCommand(ElasticsearchBaseCommand):
    syntax = 'Packages/Text/Plain text.tmLanguage'


# ---------------------------------------------------------------------
# Cat APIs
# ---------------------------------------------------------------------


class ElasticsearchCatAliasesCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'aliases')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatAllocationCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'allocation')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatHealthCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'health')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatIndicesCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'indices')
        self.request_get(path, params=dict(v=1, ts=0))


class ElasticsearchCatMasterCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'master')
        self.request_get(path, params=dict(v=1, ts=0))


class ElasticsearchCatNodesCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'nodes')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatPendingTasksCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'pending_tasks')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatPluginsCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'plugins')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatRecoveryCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'recovery')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatSegmentsCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'segments')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatShardsCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'shards')
        self.request_get(path, params=dict(v=1))


class ElasticsearchCatThreadPoolCommand(ReusltTextCommand):

    def run(self):
        path = make_path('_cat', 'thread_pool')
        self.request_get(path, params=dict(v=1))


# ---------------------------------------------------------------------
# Document APIs
# ---------------------------------------------------------------------


class ElasticsearchDeleteDocumentCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_document:
            self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return
        path = make_path(self.index, self.doc_type, document_id)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchGetDocumentCommand(ReusltJsonCommand):

    def run(self):
        self.get_document_id(self.on_done)

    def on_done(self, document_id):
        if not document_id:
            return

        path = make_path(self.index, self.doc_type, document_id)
        self.request_get(path, params=DEFAULT_PARAMS)


class ElasticsearchIndexDocumentCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_index_document:
            self.get_document_id(self.on_done)

    def on_done(self, document_id):
        path = make_path(self.index, self.doc_type, document_id)
        body = self.get_selection()
        if document_id:
            self.request_put(path, body=body, params=DEFAULT_PARAMS)
        else:
            self.request_post(path, body=body, params=DEFAULT_PARAMS)


# ---------------------------------------------------------------------
# Indices APIs
# ---------------------------------------------------------------------


class ElasticsearchAnalyzeCommand(ReusltJsonCommand):

    def run(self):
        self.get_analyzer(self.on_done)

    def on_done(self, analyzer):
        path = make_path(self.index, '_analyze')
        body = self.get_selection()
        params = DEFAULT_PARAMS
        params.update(dict(analyzer=analyzer))
        self.request_post(path, body=body, params=params)


class ElasticsearchCreateIndexCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_create_index:
            self.get_index(self.on_done)

    def on_done(self, index):
        if not index:
            return
        path = make_path(index)
        self.request_put(path, params=DEFAULT_PARAMS)


class ElasticsearchDeleteIndexCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_index:
            self.get_index(self.on_done)

    def on_done(self, index):
        if not index:
            return
        path = make_path(index)
        self.request_delete(path, params=DEFAULT_PARAMS)


class ElasticsearchDeleteMappingCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_mapping:
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
        if self.enabled_put_mapping:
            self.get_doc_type(self.on_done)

    def on_done(self, doc_type):
        if not doc_type:
            return
        path = make_path(self.index, '_mapping', doc_type)
        body = self.get_selection()
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchPutWarmerCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_put_warmer:
            self.get_warmer(self.on_done)

    def on_done(self, name):
        if not name:
            return
        path = make_path(self.index, '_warmer', name)
        body = self.get_selection()
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchDeleteWarmerCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_warmer:
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


# ---------------------------------------------------------------------
# Search APIs
# ---------------------------------------------------------------------


class ElasticsearchSearchCommand(ReusltJsonCommand):

    search_types = {
        'Search Type: Count': 'count',
        'Search Type: Dfs, Query And Fetch': 'dfs_query_and_fetch',
        'Search Type: Dfs, Query Then Fetch': 'dfs_query_then_fetch',
        'Search Type: Query And Fetch': 'query_and_fetch',
        'Search Type: Query Then Fetch (default)': 'query_then_fetch',
    }

    selected_index = 4

    def run(self):
        if self.ask_to_search_types:
            self.select_panel(self.on_done)
        else:
            self.on_done(self.selected_index)

    def select_panel(self, callback):
        search_types = list(self.search_types.keys())
        search_types.sort()
        self.window.show_quick_panel(
            search_types, callback, selected_index=self.selected_index)

    def on_done(self, index):
        if index == -1:
            return
        self.selected_index = index
        search_types = list(self.search_types.keys())
        search_types.sort()
        selected = search_types[index]
        search_type = self.search_types[selected]
        path = make_path(self.index, self.doc_type, '_search')
        body = self.get_selection()
        params = DEFAULT_PARAMS
        params.update(dict(search_type=search_type))
        self.request_post(path, body=body, params=params)


class ElasticsearchBenchmarkCommand(ReusltJsonCommand):

    def run(self):
        path = make_path('_bench')
        body = self.get_selection()
        self.request_put(path, body=body, params=DEFAULT_PARAMS)


class ElasticsearchDeletePercolatorCommand(ReusltJsonCommand):

    def run(self):
        if self.enabled_delete_percolator:
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
        if self.enabled_register_query:
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


# ---------------------------------------------------------------------
# Utility Commands
# ---------------------------------------------------------------------

class SwitchServersCommand(ElasticsearchBaseCommand):
    syntax = 'Packages/Text/Plain text.tmLanguage'
    selected_index = 0

    def run(self):
        self.select_panel(self.on_done)

    def select_panel(self, callback):
        servers = list(self.servers.keys())
        servers.sort()
        self.window.show_quick_panel(
            servers, self.on_done, selected_index=self.selected_index)

    def on_done(self, index):
        if index == -1:
            return
        self.selected_index = index
        servers = list(self.servers.keys())
        servers.sort()
        selected = servers[index]
        self.settings.set('active_server', selected)
        self.save_settings()
        self.show_active_server_settings()


class ShowActiveServerCommand(ElasticsearchBaseCommand):
    syntax = 'Packages/Text/Plain text.tmLanguage'

    def run(self):
        self.show_active_server_settings()


class ApacheBenchCommand(ElasticsearchBaseCommand):
    syntax = 'Packages/Text/Plain text.tmLanguage'
    selected_index = 0

    def run(self):
        self.select_panel(self.on_done)

    def select_panel(self, callback):
        benchmarks = list(self.benchmarks.keys())
        benchmarks.sort()
        self.window.show_quick_panel(
            benchmarks, callback, selected_index=self.selected_index)

    def run_apache_bench(self, path,
                         requests='100', concurrency='10', postfile=''):
        url = self.get_request_url(path)
        command = [self.ab_command, '-n', requests, '-c', concurrency,
                   '-p', postfile, '-T', 'application/json', url]

        for k, v in self.http_headers.items():
            command += ['-H', "{0}: {1}".format(k, v)]

        self.run_command(command)

    def on_done(self, index):
        if index == -1:
            return
        self.selected_index = index
        benchmarks = list(self.benchmarks.keys())
        benchmarks.sort()
        selected = benchmarks[index]
        benchmark = self.benchmarks[selected]
        requests = str(benchmark.get('requests'))
        concurrency = str(benchmark.get('concurrency'))
        path = make_path(self.index, self.doc_type, '_search')
        postfile = self.get_file_name()
        self.run_apache_bench(path, requests, concurrency, postfile)


class AutoPrettyFormat(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        settings = view.settings()
        pretty_command = settings.get('pretty_command')
        enabled_pretty = settings.get('enabled_pretty')
        pretty_syntax = "{}.tmLanguage".format(settings.get('pretty_syntax'))
        view_syntax = settings.get('syntax')

        if enabled_pretty and view_syntax.endswith(pretty_syntax):
            view.run_command(pretty_command)


class SearchDocsCommand(sublime_plugin.WindowCommand):

    def search_docs(self, text):
        params = {'q': text}
        url = "https://www.elastic.co/search?{}".format(urlencode(params))
        self.window.run_command('open_url', {'url': url})

    def run(self):
        self.window.show_input_panel(
            'Search:', '', self.search_docs, None, None)
