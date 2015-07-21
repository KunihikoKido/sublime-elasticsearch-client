from .base import BaseCommand


class IndicesGetTemplateCommand(BaseCommand):
    command_name = "elasticsearch:indices-get-template"

    def is_enabled(self):
        return True

    def run_request(self, name=None):
        if name is None:
            self.show_index_template_list_panel(self.run)
            return

        options = dict(
            name=name
        )

        return self.client.indices.get_template(**options)
