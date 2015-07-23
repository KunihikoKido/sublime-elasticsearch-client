from .base import BaseCommand


class GetDocumentSourceCommand(BaseCommand):
    command_name = "elasticsearch:get-document-source"

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

        return self.client.get_source(**options)
