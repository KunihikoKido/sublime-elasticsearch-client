import sublime


class SnapshotListPanel(object):

    def __init__(self, window, client, repository):
        self.window = window
        self.client = client
        self.repository = repository
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        self.callback(
            repository=self.repository,
            snapshot=self.choices[index][0],
            indices=self.choices[index][1].split(","))

    def show(self, callback):
        self.callback = callback

        options = dict(
            repository=self.repository,
            snapshot="_all"
        )

        try:
            response = self.client.snapshot.get(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices = []
        for snapshot in response["snapshots"]:
            self.choices.append([
                snapshot["snapshot"],
                ",".join(snapshot["indices"])
                ])
        self.choices.sort(reverse=True)
        self.window.show_quick_panel(self.choices, self.on_done)
