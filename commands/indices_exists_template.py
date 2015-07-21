from .base import BaseCommand


class IndicesExistsTemplateCommand(BaseCommand):
    command_name = "elasticsearch:indices-exists-template"

    def is_enabled(self):
        return True

    def run_request(self, name=None):
        if not name:
            self.show_input_panel('Index Template Name: ', '', self.run)
            return

        options = dict(
            name=name
        )

        return self.client.indices.exists_template(**options)
