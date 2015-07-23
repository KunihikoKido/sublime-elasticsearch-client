import sublime
from .base import DeleteBaseCommand


class IndicesDeleteAliasCommand(DeleteBaseCommand):
    command_name = "elasticsearch:indices-delete-alias"

    def is_enabled(self):
        return True

    def run_request(self, index=None, name=None):
        if not index or not name:
            self.show_alias_list_panel(self.run)
            return

        options = dict(
            index=index,
            name=name
        )

        if sublime.ok_cancel_dialog("Are you sure you want to delete?", ok_title='Delete'):
            return self.client.indices.delete_alias(**options)
