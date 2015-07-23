from .base import CreateBaseCommand


class HelperChangeNumberOfReplicasCommand(CreateBaseCommand):
    command_name = "elasticsearch:helper-change-number-of-replicas"

    def is_enabled(self):
        return True

    def show_input_replicas(self, label, default, index, callback):
        def on_done(replicas):
            callback(index=index, replicas=replicas)

        self.window.show_input_panel(label, default, on_done, None, None)

    def run_request(self, index=None, replicas=None):
        if not index:
            self.show_index_list_panel(self.run)
            return

        if not replicas:
            self.show_input_replicas(
                "Number Of Replicas: ", "", index, self.run)
            return

        options = dict(
            index=index,
            body={
                "index": {
                    "number_of_replicas": replicas
                }
            }
        )

        self.client.indices.put_settings(**options)
        self.window.run_command('cat_indices', {'index': index})

