from .base import BaseCommand


class IndicesGetFieldMappingCommand(BaseCommand):
    command_name = "elasticsearch:indices-get-field-mapping"

    def is_enabled(self):
        return True

    def run_request(self, field=None):
        if field is None:
            self.show_field_list_panel(self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            field=field
        )

        return self.client.indices.get_field_mapping(**options)
