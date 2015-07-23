from .base import BaseCommand


class SearchPercolatorQueryCommand(BaseCommand):
    command_name = "elasticsearch:search-percolator-query"

    def is_enabled(self):
        return True

    def query_dsl(self, query):
        query_dsl = {
            "query": {
                "prefix": {
                    "_id": query
                }
            }
        }
        return query_dsl

    def run_request(self, query=None):
        if query is None:
            self.show_input_panel(
                'Prefix search for percolator query id (option): ',
                '', self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=".percolator",
            body=self.query_dsl(query)
        )

        return self.client.search(**options)
