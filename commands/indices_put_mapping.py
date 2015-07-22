from .base import CreateBaseCommand


class IndicesPutMappingCommand(CreateBaseCommand):
    command_name = "elasticsearch:indices-put-mapping"

    def run_request(self, doc_type=None):
        if not doc_type:
            self.show_input_panel(
                'Document type name: ', self.settings.doc_type, self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=doc_type,
            body=self.get_text()
        )

        return self.client.indices.put_mapping(**options)
