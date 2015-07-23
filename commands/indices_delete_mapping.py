import sublime
from .base import DeleteBaseCommand


class IndicesDeleteMappingCommand(DeleteBaseCommand):
    command_name = "elasticsearch:indices-delete-mapping"

    def is_enabled(self):
        return True

    def run_request(self, index=None, doc_type=None):
        index = index or self.settings.index

        if not doc_type:
            self.show_doc_type_list_panel(self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=doc_type
        )

        if sublime.ok_cancel_dialog("Are you sure you want to delete?", ok_title='Delete'):
            return self.client.indices.delete_mapping(**options)
