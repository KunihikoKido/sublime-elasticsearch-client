from .base import BaseCommand


class GetPercolatorQueryCommand(BaseCommand):
    command_name = "elasticsearch:get-percolator-query"

    def is_enabled(self):
        return True

    def run_request(self, id=None):
        if not id:
            self.show_input_panel('Percolator Query Id: ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=".percolator",
            id=id
        )

        return self.client.get_source(**options)
