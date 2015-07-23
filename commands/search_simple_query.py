from .base import BaseCommand


class SearchSimpleQueryCommand(BaseCommand):
    command_name = "elasticsearch:search-simple-query"

    def is_enabled(self):
        return True

    def run_request(self, query=None):
        if query is None:
            self.show_input_panel('Query: ', '*', self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            params=dict(q=query)
        )

        return self.client.search(**options)
