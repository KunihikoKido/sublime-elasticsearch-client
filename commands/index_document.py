import sublime
from .base import BaseCommand


class IndexDocumentCommand(BaseCommand):

    def run_request(self, id=None):
        if id is None:
            return self.show_input_panel(
                'Document Id (option): ', '', self.run_request)

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            id=id
        )

        try:
            response = self.client.index(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        return self.show_object_output_panel(response)
