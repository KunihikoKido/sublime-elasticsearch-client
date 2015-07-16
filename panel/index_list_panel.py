import sublime


class IndexListPanel(object):

    def __init__(self, window, client):
        self.window = window
        self.client = client
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        self.callback(index=self.choices[index])

    def show(self, callback):
        self.callback = callback

        options = dict()

        try:
            response = self.client.cluster.state(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices = list(response["metadata"]["indices"].keys())

        self.window.show_quick_panel(self.choices, self.on_done)
