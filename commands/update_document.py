from .base import CreateBaseCommand


class UpdateDocumentCommand(CreateBaseCommand):
    command_name = "elasticsearch:update-document"

    def run_request(self, id=None):
        if not id:
            self.show_input_panel("Document Id: ", "", self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            id=id,
            body=self.get_text()
        )
        return self.client.update(**options)
