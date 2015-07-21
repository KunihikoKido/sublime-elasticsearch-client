import sublime
from .base import DeleteBaseCommand


class DeleteByQueryCommand(DeleteBaseCommand):
    command_name = "elasticsearch:delete-by-query"

    def run_request(self):

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text()
        )

        if sublime.ok_cancel_dialog("Are you sure you want to delete?", ok_title='Delete'):
            return self.client.delete_by_query(**options)
