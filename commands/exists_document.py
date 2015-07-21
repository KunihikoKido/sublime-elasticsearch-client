from .base import BaseCommand


class ExistsDocumentCommand(BaseCommand):
    command_name = "elasticsearch:exists-document"

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

        return self.client.exists(**options)
