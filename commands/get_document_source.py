import sublime
from .base import BaseCommand


class GetDocumentSourceCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self, id=None):
        if not id:
            return self.show_input_panel(
                'Document Id: ', '', self.run_request)

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            id=id
        )

        try:
            response = self.client.get_source(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        return self.show_response(response)
