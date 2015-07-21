from .base import CreateBaseCommand


class IndicesCreateDocTypeCommand(CreateBaseCommand):
    command_name = "elasticsearch:indices-close"

    def is_enabled(self):
        return True

    def run_request(self, doc_type=None):
        if not doc_type:
            self.show_input_panel(
                'Document type name: ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=doc_type,
            body={doc_type: {}}
        )

        print(options)

        return self.client.indices.put_mapping(**options)
