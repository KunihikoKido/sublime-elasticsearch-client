import sublime


class IndexListPanel(object):

    def __init__(self, window, client, default_index=None):
        self.window = window
        self.client = client
        self.default_index = default_index
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        self.callback(index=self.choices[index])

    def show(self, callback):
        self.callback = callback

        options = dict(ignore=[403])

        try:
            response = self.client.cluster.state(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices.append(self.default_index)
        if "metadata" in response.keys():
            for index in list(response["metadata"]["indices"].keys()):
                if index != self.default_index:
                    self.choices.append(index)

        self.choices.sort()
        self.window.show_quick_panel(self.choices, self.on_done)
