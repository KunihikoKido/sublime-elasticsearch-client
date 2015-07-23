from .base import CreateBaseCommand


class IndicesPutSettingsCommand(CreateBaseCommand):
    command_name = "elasticsearch:indices-put-settings"

    def run_request(self, index=None):
        if not index:
            self.show_input_panel(
                'Index name: ', self.settings.index, self.run)
            return

        options = dict(
            index=self.settings.index,
            body=self.get_text()
        )

        return self.client.indices.put_settings(**options)
