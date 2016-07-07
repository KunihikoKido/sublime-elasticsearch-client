from .base import CreateBaseCommand


class CreateDocumentCommand(CreateBaseCommand):
    command_name = "elasticsearch:create-document"

    def is_enabled(self):
        return True

    def run_request(self, id=None):
        if not id:
            self.show_input_panel(
                'Document Id : ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            id=id
        )

        return self.client.create(**options)
