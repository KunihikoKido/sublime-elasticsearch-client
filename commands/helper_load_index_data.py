import sublime
import json
from elasticsearch.helpers import bulk_index
from .base import CreateBaseCommand


def readlines_chunks(file, chunk_size=1024 * 1024):
    while True:
        lines = file.readlines(chunk_size)
        if not lines:
            break

        docs = []
        for doc in lines:
            docs.append(json.loads(doc))
        yield docs


def change_doc_index(docs, index):
    for doc in docs:
        doc['_index'] = index
        yield doc


def expand_action(data):
    data = data.copy()
    op_type = data.pop('_op_type', 'index')
    action = {op_type: {}}
    for key in ('_parent', '_percolate', '_routing', '_timestamp',
                '_ttl', '_type', '_version', '_version_type',
                '_id', '_retry_on_conflict'):
        if key in data:
            action[op_type][key] = data.pop(key)

    # no data payload for delete
    if op_type == 'delete':
        return action, None

    return action, data.get('_source', data)


class HelperLoadIndexDataCommand(CreateBaseCommand):
    command_name = "elasticsearch:helper-load-index-data"

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
                "Open: ", self.settings.dump_file, index, self.run)
            return

        count = 0
        with open(filename, encoding='utf-8', mode='r') as f:
            for docs in readlines_chunks(f):
                options = dict(
                    index=index,
                    stats_only=False,
                    chunk_size=self.settings.chunk_size,
                    expand_action_callback=expand_action
                )

                success, errors = bulk_index(
                    self.client, change_doc_index(docs, index), **options)

                if errors:
                    return dict(
                        command=self.command_name,
                        index=index,
                        filename=filename,
                        status="ERROR",
                        errors=errors
                    )

                count += success
                sublime.status_message("Load: {}".format(count))

        return dict(
            command=self.command_name,
            index=index,
            filename=filename,
            status="SUCCESS",
            docs=count
        )
