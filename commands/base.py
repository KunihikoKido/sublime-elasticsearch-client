import json
import threading
import sublime
import sublime_plugin
from elasticsearch import Elasticsearch
from elasticsearch import Urllib3HttpConnection

from ..panel import IndexListPanel
from ..panel import DocTypeListPanel
from ..panel import SwitchServerListPanel


class CustomConnection(Urllib3HttpConnection):
    def __init__(self, host='localhost', port=80, headers=None, **kwargs):
        super(CustomConnection, self).__init__(host=host, port=port, **kwargs)
        if headers is not None:
            self.headers.update(headers)


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
    def headers(self):
        return self.settings.get("headers", None)

    @property
    def servers(self):
        return self.settings.get("servers", [])

    @property
    def active_server(self):
        return dict(
            base_url=self.base_url,
            index=self.index,
            doc_type=self.doc_type,
            scroll_size=self.scroll_size,
        )

    def set(self, key, value):
        self.settings.set(key, value)

    def save(self):
        sublime.save_settings(self.SETTINGS_FILE)


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
        return self.view.substr(sublime.Region(0, self.view.size()))

    def init_client(self):
        self._client = Elasticsearch(
            self.settings.base_url,
            connection_class=CustomConnection,
            headers=self.settings.headers
        )
        return self._client

    def save_settings(self):
        self.settings.save()
        self.init_client()

    @property
    def client(self):
        return self.init_client()

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

    def show_switch_server_list_panel(self, callback):
        list_panel = SwitchServerListPanel(
            self.window, self.settings.servers)
        list_panel.show(callback)

    def show_output_panel(self, text, syntax="Packages/Text/Plain text.tmLanguage"):
        panel = self.window.create_output_panel("elasticsearch")
        self.window.run_command(
            "show_panel", {"panel": "output.elasticsearch"})
        panel.set_syntax_file(syntax)
        panel.settings().set('gutter', True)
        panel.settings().set('word_wrap', False)
        panel.set_read_only(False)
        panel.run_command('append', {'characters': text})
        panel.set_read_only(True)

    def show_active_server(self):
        self.window.run_command("settings_show_active_server")

    def request_thread(self, *args, **kwargs):
        thread = threading.Thread(
            target=self.run_request, args=args, kwargs=kwargs)
        thread.start()

    def run(self, *args, **kwargs):
        self.request_thread(*args, **kwargs)
