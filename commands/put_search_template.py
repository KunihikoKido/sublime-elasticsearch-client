from .base import CreateBaseCommand


class PutSearchTemplateCommand(CreateBaseCommand):
    command_name = "elasticsearch:put-search-template"

    def run_request(self, template_id=None):
        if not template_id:
            self.show_input_panel(
                'Search Template Id: ', '', self.run)
            return

        options = dict(
            id=template_id,
            body=self.get_text()
        )

        return self.client.put_template(**options)
