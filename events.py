import sublime
import sublime_plugin


class ActiveServerStatusBar(sublime_plugin.EventListener):
    SETTINGS_FILE = 'Elasticsearch.sublime-settings'

    def update_status_bar(self, view):
        sublime.set_timeout_async(lambda: self._update_status_bar(view))

    def _update_status_bar(self, view):
        settings = sublime.load_settings(self.SETTINGS_FILE)

        base_url = settings.get("base_url")
        index = settings.get("index")
        doc_type = settings.get("doc_type")

        options = dict(
            base_url=base_url,
            index=index,
            doc_type=doc_type
        )

        if view is not None:
            view.set_status(
                "elasticsearch-client",
                "Elasticsearch: {base_url}".format(**options))

    def on_new(self, view):
        self.update_status_bar(view)

    def on_load(self, view):
        self.update_status_bar(view)

    def on_activated(self, view):
        self.update_status_bar(view)

    def on_deactivated(self, view):
        self.update_status_bar(view)

    def on_post_save(self, view):
        self.update_status_bar(view)

    def on_pre_close(self, view):
        self.update_status_bar(view)

    def on_window_command(self, window, command_name, args):
        self.update_status_bar(window.active_view())
