import sublime
from .base import DeleteBaseCommand


class IndicesDeleteTemplateCommand(DeleteBaseCommand):
    command_name = "elasticsearch:indices-delete-template"

    def is_enabled(self):
        return True

    def run_request(self, name=None):
        if not name:
            self.show_index_template_list_panel(self.run)
            return

        options = dict(
            name=name
        )

        if sublime.ok_cancel_dialog("Are you sure you want to delete?", ok_title='Delete'):
            return self.client.indices.delete_template(**options)
