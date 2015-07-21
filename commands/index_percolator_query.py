from .base import CreateBaseCommand


class IndexPercolatorQueryCommand(CreateBaseCommand):
    command_name = "elasticsearch:index-percolator-query"

    def run_request(self, id=None):
        if id is None:
            self.show_input_panel(
                'Percolator Query Id (option): ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=".percolator",
            body=self.get_text(),
            id=id
        )

        return self.client.index(**options)
