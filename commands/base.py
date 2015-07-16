import json
import threading
import sublime
import sublime_plugin
from elasticsearch import Elasticsearch
from ..panel import IndexListPanel
from ..panel import DocTypeListPanel


class Settings(object):
    SETTINGS_FILE = 'Elasticsearch.sublime-settings'

    def __init__(self):
        self.settings = sublime.load_settings(self.SETTINGS_FILE)

    @property
    def base_url(self):
        return self.settings.get("base_url", "http://localhost:9200")

    @property
    def index(self):
        return self.settings.get("index", "blog-ja")

    @property
    def doc_type(self):
        return self.settings.get("doc_type", "posts")

    @property
    def scroll_size(self):
        return self.settings.get("scroll_size", "1m")

    @property
    def servers(self):
        return self.settings.get("servers", [])


class BaseCommand(sublime_plugin.WindowCommand):

    def __init__(self, *args, **kwargs):
        self.settings = Settings()
        sublime_plugin.WindowCommand.__init__(self, *args, **kwargs)

    @property
    def view(self):
        return self.window.active_view()

    def is_valid_json(self):
        try:
            json.loads(self.get_text())
        except ValueError:
            return False
        return True

    def is_enabled(self):
        return self.is_valid_json()

    def get_text(self):
        text = self.view.substr(sublime.Region(0, self.view.size()))
        return text

    def init_client(self):
        self._client = Elasticsearch(self.settings.base_url)

    @property
    def client(self):
        if hasattr(self, "_client"):
            return self._client
        self.init_client()
        return self.client

    def show_response(self, response, title=""):
        title = title or self.__class__.__name__
        text = json.dumps(response, indent=2, ensure_ascii=False)
        self.window.run_command(
            "show_response", {
                "title": title,
                "text": text
            }
        )

    def show_index_list_panel(self, callback):
        list_panel = IndexListPanel(self.window, self.client)
        list_panel.show(callback)

    def show_doc_type_list_panel(self, callback):
        list_panel = DocTypeListPanel(
            self.window, self.client, self.settings.index)
        list_panel.show(callback)

    def request_thread(self, *args, **kwargs):
        thread = threading.Thread(
            target=self.run_request, args=args, kwargs=kwargs)
        thread.start()

    def run(self, *args, **kwargs):
        self.request_thread(*args, **kwargs)
