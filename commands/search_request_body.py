import sublime
from .base import BaseCommand


class SearchRequestBodyCommand(BaseCommand):

    def make_options(self, search_type=None):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            params={},
            ignore=[404, 400]
        )

        if search_type == "scan":
            options["params"] = dict(
                search_type=search_type,
                scroll=self.settings.scroll_size
            )
        elif search_type is not None:
            options["params"] = dict(
                search_type=search_type
            )
        return options

    def run_request(self, search_type=None):
        options = self.make_options(search_type=search_type)

        try:
            response = self.client.search(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        return self.show_response(response)
