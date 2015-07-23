from .base import BaseCommand


class IndicesExistsDocTypeCommand(BaseCommand):
    command_name = "elasticsearch:indices-exists-doc-type"

    def is_enabled(self):
        return True

    def run_request(self, doc_type=None):
        if not doc_type:
            self.show_input_panel('Document Type Name: ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=doc_type
        )

        return self.client.indices.exists_type(**options)
