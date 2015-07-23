import sublime
from elasticsearch.helpers import reindex
from .base import CreateBaseCommand


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


class HelperReindexCommand(CreateBaseCommand):
    command_name = "elasticsearch:helper-reindex"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if not index:
            self.show_index_list_panel(self.run)
            return

        if not sublime.ok_cancel_dialog(
           "Are you sure you want to reindex?", ok_title='Reindex'):
            return

        sublime.status_message("Reindex: start ... please waite.")

        options = dict(
            client=self.client,
            source_index=index,
            target_index=index,
            target_client=self.client,
            chunk_size=self.settings.chunk_size,
            scroll=self.settings.scroll_size,
            scan_kwargs=dict(),
            bulk_kwargs=dict(
                index=index,
                stats_only=False,
                expand_action_callback=expand_action
            )
        )

        success, errors = reindex(**options)

        if errors:
            return dict(
                command=self.command_name,
                index=index,
                status="ERROR",
                errors=errors
            )

        return dict(
            command=self.command_name,
            index=index,
            status="SUCCESS",
            docs=success
        )
