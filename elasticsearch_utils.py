"""
Utils Commands for Elasticsearch Client for sublime text 3
"""

import sublime_plugin
from urllib.parse import urlencode
from .elasticsearch import ElasticsearchBaseCommand
from .elasticsearch import make_path


class SwitchServersCommand(ElasticsearchBaseCommand):
    syntax = 'Packages/YAML/YAML.tmLanguage'
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
    syntax = 'Packages/YAML/YAML.tmLanguage'

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

    def make_path(self):
        return make_path(self.index, self.doc_type, '_search')

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
        path = self.make_path()
        postfile = self.get_file_name()
        self.run_apache_bench(path, requests, concurrency, postfile)


class SearchTemplateApacheBenchCommand(ApacheBenchCommand):
    """ Apache Bentch for Search Template Query """

    def make_path(self):
        return make_path(self.index, self.doc_type, '_search', 'template')


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
