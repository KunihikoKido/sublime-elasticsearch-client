from .base import CreateBaseCommand


class IndicesPutWarmerCommand(CreateBaseCommand):
    command_name = "elasticsearch:indices-put-warmer"

    def run_request(self, name=None):
        if not name:
            self.show_input_panel(
                'Warmer Name: ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            name=name,
            body=self.get_text()
        )

        return self.client.indices.put_warmer(**options)
