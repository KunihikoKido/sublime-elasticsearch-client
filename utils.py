import sublime
import sublime_plugin
from .base import BaseElasticsearchCommand
from .base import make_path
from .base import DEFAULT_PARAMS


__all__ = ["SwitchServersCommand", "ShowActiveServerCommand",
           "ChangeIndexSettingCommand", "ChangeDocTypeSettingCommand",
           "ApacheBenchCommand", "AutoPrettyFormat"]


class SwitchServersCommand(BaseElasticsearchCommand):

    def run(self):
        super(SwitchServersCommand, self).run()
        servers = list(self.servers.keys())
        servers.sort()
        self.window.show_quick_panel(servers, self.server_selected)

    def server_selected(self, index):
        if index == -1:
            sublime.status_message('Canceled')
            return  # canceled
        self.active_server = list(self.servers.keys())[index]
        self.settings.set("active_server", self.active_server)
        self.save_settings()
        self.status_message("Switched: {0}".format(self.active_server))


class ShowActiveServerCommand(BaseElasticsearchCommand):

    def run(self):
        super(ShowActiveServerCommand, self).run()
        self.panel(
            "Active Server Settings [{active_server}]\n"
            "=============================================================\n"
            "- base_url                     : {base_url}\n"
            "- index                        : {index}\n"
            "- doc_type                     : {doc_type}\n"
            "- analyzer                     : {analyzer}\n"
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
                enabled_register_query=self.enabled_register_query)
        )

        self.status_message(
            ': {0} ({1} / {2})'.format(
                self.active_server, self.index, self.doc_type))


class ChangeIndexSettingCommand(BaseElasticsearchCommand):

    def run(self):
        super(ChangeIndexSettingCommand, self).run()
        self.get_index(self.set_index)


class ChangeDocTypeSettingCommand(BaseElasticsearchCommand):

    def run(self):
        super(ChangeDocTypeSettingCommand, self).run()
        self.get_doc_type(self.set_doc_type)


class ApacheBenchCommand(BaseElasticsearchCommand):

    def run(self):
        super(ApacheBenchCommand, self).run()

        self.select_benchmark(self.run_benchmark)

    def select_benchmark(self, callback):
        benchmarks = list(self.benchmarks.keys())
        self.window.show_quick_panel(benchmarks, callback)

    def run_benchmark(self, index):
        if index == -1:
            self.status_message('Canceled')
            return  # canceled

        selected = list(self.benchmarks.keys())[index]
        benchmark = self.benchmarks[selected]
        requests = benchmark.get('requests')
        concurrency = benchmark.get('concurrency')
        filename = self.filename
        url = make_path(self.index, self.doc_type, '_search')
        request_url = self.get_request_url(url, DEFAULT_PARAMS)

        command = [self.ab_command, '-n', str(requests),
                   '-c', str(concurrency), request_url]
        if filename:
            command = [self.ab_command, '-n', str(requests),
                       '-c', str(concurrency), '-p', filename,
                       '-T', 'application/json', request_url]

        self.window.run_command('exec', {'cmd': command, 'quiet': self.quiet})


class AutoPrettyFormat(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        settings = view.settings()
        pretty_command = settings.get('pretty_command')
        enabled_pretty = settings.get('enabled_pretty')
        pretty_syntax = "{}.tmLanguage".format(settings.get('pretty_syntax'))
        view_syntax = settings.get('syntax')

        if enabled_pretty and view_syntax.endswith(pretty_syntax):
            view.run_command(pretty_command)
