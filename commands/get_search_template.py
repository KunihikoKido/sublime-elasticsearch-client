import sublime
from .base import BaseCommand


class GetSearchTemplateCommand(BaseCommand):
    command_name = "elasticsearch:get-search-template"

    def is_enabled(self):
        return True

    def run_request(self, id=None):
        if not id:
            self.show_search_template_list_panel(self.run)
            return

        options = dict(
            id=id
        )
        print(options)

        return self.client.get_template(**options)
