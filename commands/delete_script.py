import sublime
from .base import DeleteBaseCommand


class DeleteScriptCommand(DeleteBaseCommand):
    command_name = "elasticsearch:delete-script"

    def is_enabled(self):
        return True

    def run_request(self, lang=None, id=None):
        if not lang or not id:
            self.show_script_list_panel(self.run)
            return

        options = dict(
            lang=lang,
            id=id
        )

        if sublime.ok_cancel_dialog("Are you sure you want to delete?", ok_title='Delete'):
            return self.client.delete_script(**options)
