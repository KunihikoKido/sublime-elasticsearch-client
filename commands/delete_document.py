import sublime
from .base import DeleteBaseCommand


class DeleteDocumentCommand(DeleteBaseCommand):
    command_name = "elasticsearch:delete-document"

    def is_enabled(self):
        return True

    def run_request(self, id=None):
        if not id:
            self.show_input_panel('Document Id: ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            id=id
        )

        if sublime.ok_cancel_dialog("Are you sure you want to delete?", ok_title='Delete'):
            return self.client.delete(**options)
