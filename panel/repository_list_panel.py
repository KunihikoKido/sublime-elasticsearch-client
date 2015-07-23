import sublime


class RepositoryListPanel(object):

    def __init__(self, window, client, **kwargs):
        self.window = window
        self.client = client
        self.kwargs = kwargs
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        self.callback(repository=self.choices[index][0], **self.kwargs)

    def show(self, callback):
        self.callback = callback

        options = dict()

        try:
            response = self.client.snapshot.get_repository(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices = []
        for repository, info in response.items():
            self.choices.append([repository, info["type"]])
        self.choices.sort()
        self.window.show_quick_panel(self.choices, self.on_done)
