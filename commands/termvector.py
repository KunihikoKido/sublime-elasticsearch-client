from .base import BaseCommand


class TermvectorCommand(BaseCommand):
    command_name = "elasticsearch:termvector"

    def run_request(self, id=None):
        if id is None:
            self.show_input_panel("Document Id (option): ", "", self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            id=id,
            body=self.get_text()
        )
        return self.client.termvector(**options)
