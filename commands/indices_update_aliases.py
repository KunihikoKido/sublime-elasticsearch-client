from .base import CreateBaseCommand


class IndicesUpdateAliasesCommand(CreateBaseCommand):
    command_name = "elasticsearch:indices-update-aliases"

    def run_request(self):
        options = dict(
            body=self.get_text()
        )

        return self.client.indices.update_aliases(**options)
