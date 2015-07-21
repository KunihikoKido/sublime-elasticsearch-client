import sublime
from .base import DeleteBaseCommand


class DeleteSearchTemplateCommand(DeleteBaseCommand):
    command_name = "elasticsearch:delete-search-template"

    def is_enabled(self):
        return True

    def run_request(self, id=None):
        if not id:
            self.show_search_template_list_panel(self.run)
            return

        options = dict(
            id=id
        )

        if sublime.ok_cancel_dialog("Are you sure you want to delete?", ok_title='Delete'):
            return self.client.delete_template(**options)
