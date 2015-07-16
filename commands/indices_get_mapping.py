import sublime
from .base import BaseCommand


class IndicesGetMappingCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self, doc_type=None):
        if doc_type is None:
            return self.show_doc_type_list_panel(self.run_request)

        options = dict(
            index=self.settings.index,
            doc_type=doc_type
        )
        print(options)

        try:
            response = self.client.indices.get_mapping(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        return self.show_response(response)
