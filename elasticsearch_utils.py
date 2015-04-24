"""
Utils Commands for Elasticsearch Client for sublime text 3
"""

import sublime_plugin
from urllib.parse import urlencode
from .elasticsearch import ElasticsearchBaseCommand
from .elasticsearch import make_path
from .elasticsearch import make_url


class SwitchServersCommand(ElasticsearchBaseCommand):
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
        self.window.run_command('show_active_server')


class ShowActiveServerCommand(ElasticsearchBaseCommand):
    syntax = 'Packages/JavaScript/JSON.tmLanguage'

    def run(self):
        self.show_result({self.active_server: self.server_settings})


class ApacheBenchCommand(ElasticsearchBaseCommand):

    selected_index = 0

    def run(self):
        self.select_panel(self.on_done)

    def select_panel(self, callback):
        ab_options = list(self.ab_options.keys())
        ab_options.sort()
        self.window.show_quick_panel(
            ab_options, callback, selected_index=self.selected_index)

    def apache_bench(self, path, ab_options, postfile):
        url = make_url(self.base_url, path)
        command = [self.ab_command]
        command += ab_options

        for k, v in self.http_headers.items():
            command += ['-H', "{0}: {1}".format(k, v)]

        command += ['-p', postfile]
        command += [url]
        self.window.run_command('exec', {'cmd': command})

    def make_path(self):
        return make_path(self.index, self.doc_type, '_search')

    def get_ab_options(self, index):
        ab_options = list(self.ab_options.keys())
        ab_options.sort()
        selected = ab_options[index]
        return self.ab_options[selected]

    def on_done(self, index):
        if index == -1:
            return

        self.selected_index = index

        ab_options = self.get_ab_options(index)
        path = self.make_path()
        postfile = self.get_file_name()
        self.apache_bench(path, ab_options, postfile)


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
