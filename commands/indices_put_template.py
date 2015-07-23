from .base import CreateBaseCommand


class IndicesPutTemplateCommand(CreateBaseCommand):
    command_name = "elasticsearch:indices-put-template"

    def run_request(self, name=None):
        if not name:
            self.show_input_panel(
                'Index Template Name: ', '', self.run)
            return

        options = dict(
            name=name,
            body=self.get_text()
        )

        return self.client.indices.put_template(**options)
