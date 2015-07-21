import sublime
from .base import DeleteBaseCommand


class IndicesDeleteCommand(DeleteBaseCommand):
    command_name = "elasticsearch:indices-delete"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if not index:
            self.show_index_list_panel(self.run)
            return

        options = dict(
            index=index
        )

        if sublime.ok_cancel_dialog("Are you sure you want to delete?", ok_title='Delete'):
            return self.client.indices.delete(**options)
