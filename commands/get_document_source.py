from .base import BaseCommand


class GetDocumentSourceCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self, id=None):
        if not id:
            self.show_input_panel('Document Id: ', '', self.run_request)
            return

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            id=id
        )
        response = self.client.get_source(**options)
        self.show_response(response)
