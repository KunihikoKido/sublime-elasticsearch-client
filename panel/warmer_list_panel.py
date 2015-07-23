import sublime


class WarmerListPanel(object):

    def __init__(self, window, client, index):
        self.window = window
        self.client = client
        self.index = index
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        name = self.choices[index]
        self.callback(name=name)

    def show(self, callback):
        self.callback = callback

        options = dict(
            index=self.index
        )

        try:
            response = self.client.indices.get_warmer(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices = []
        for name in response[self.index]["warmers"].keys():
            print(response[self.index])
            self.choices.append(name)
        self.choices.sort()
        self.window.show_quick_panel(self.choices, self.on_done)
