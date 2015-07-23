import csv
import sublime
from elasticsearch.helpers import bulk_index
from .base import CreateBaseCommand


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


class HelperImportCsvCommand(CreateBaseCommand):
    command_name = "elasticsearch:helper-import-csv"

    def is_enabled(self):
        return True

    def show_input_filename(self, label, default, index, doc_type, callback):
        def on_done(filename):
            callback(index=index, doc_type=doc_type, filename=filename)

        self.window.show_input_panel(label, default, on_done, None, None)

    def save_filename(self, filename):
        self.settings.set("dump_file", filename)
        self.settings.save()

    def run_request(self, index=None, doc_type=None, filename=None):
        if not index:
            self.show_index_list_panel(self.run)
            return

        if not doc_type:
            self.show_doc_type_list_panel(self.run)
            return

        if not filename:
            self.show_input_filename(
                "Open: ", '', index, doc_type, self.run)
            return

        docs = []
        with open(filename, encoding='utf-8', mode='r') as csvfile:
            for doc in csv.DictReader(csvfile, delimiter=','):
                docs.append(doc)
                sublime.status_message("Read: {}".format(len(docs)))

        options = dict(
            index=index,
            doc_type=doc_type,
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

        return dict(
            command=self.command_name,
            index=index,
            doc_type=doc_type,
            filename=filename,
            status="SUCCESS",
            docs=success
        )
