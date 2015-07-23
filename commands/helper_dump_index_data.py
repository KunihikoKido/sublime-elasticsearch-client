import sublime
import json
from .base import CreateBaseCommand
from elasticsearch.helpers import scan


class HelperDumpIndexDataCommand(CreateBaseCommand):
    command_name = "elasticsearch:helper-dump-index-data"

    def is_enabled(self):
        return True

    def show_input_filename(self, label, default, index, callback):
        def on_done(filename):
            callback(index=index, filename=filename)

        self.window.show_input_panel(label, default, on_done, None, None)

    def save_filename(self, filename):
        self.settings.set("dump_file", filename)
        self.settings.save()

    def run_request(self, index=None, filename=None):
        if not index:
            self.show_index_list_panel(self.run)
            return

        if not filename:
            self.show_input_filename(
                "Save as: ", self.settings.dump_file, index, self.run)
            return

        options = dict(
            index=index,
            scroll=self.settings.scroll_size
        )

        count = 0
        with open(filename, encoding='utf-8', mode='w') as f:
            for doc in scan(self.client, **options):
                del doc['_score']
                doc = "{}\n".format(json.dumps(doc, ensure_ascii=False))
                f.write(doc)
                count += 1
                sublime.status_message("Dump: {}".format(count))

        self.save_filename(filename)

        return dict(
            command=self.command_name,
            index=index,
            filename=filename,
            status="SUCCESS",
            docs=count
        )
