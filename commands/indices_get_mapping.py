from .base import BaseCommand


class IndicesGetMappingCommand(BaseCommand):
    command_name = "elasticsearch:indices-get-mapping"

    def is_enabled(self):
        return True

    def run_request(self, index=None, doc_type=None):
        index = index or self.settings.index

        if not doc_type:
            self.show_doc_type_list_panel(self.run)
            return

        options = dict(
            index=index,
            doc_type=doc_type
        )

        return self.client.indices.get_mapping(**options)
