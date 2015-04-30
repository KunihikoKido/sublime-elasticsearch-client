from .base import ESClientBaseCommand
from .elasticsearch import Elasticsearch
from .elasticsearch.helpers import reindex


class HelperBaseCommand(ESClientBaseCommand):
    selected_index = 0

    def select_server(self, callback):
        self.server_choices = list(self.servers.keys())
        self.server_choices.sort()
        self.window.show_quick_panel(
            self.server_choices, self.on_done,
            selected_index=self.selected_index)

    def get_server_settings(self, index):
        selected = self.server_choices[index]
        return self.servers[selected]


class ReindexCommand(HelperBaseCommand):
    result_window_title = "Reindex"
    show_result_on_window = False
    syntax = 'Packages/JavaScript/JSON.tmLanguage'

    def run(self):
        self.select_server(self.on_done)

    def on_done(self, index):
        if index == -1:
            return

        self.selected_index = index

        server = self.get_server_settings(index)
        base_url = server.get('base_url')
        headers = server.get('http_headers')
        index = server.get('index')
        client = Elasticsearch(base_url, headers)

        self.request(reindex, client, source_index=index,
                     target_index=index)
