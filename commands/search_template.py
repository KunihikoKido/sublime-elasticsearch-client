import sublime
from .search_request_body import SearchRequestBodyCommand


class SearchTemplateCommand(SearchRequestBodyCommand):

    def run_request(self, search_type=None):
        options = self.make_options(search_type=search_type)

        try:
            response = self.client.search_template(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        return self.show_response(response)
