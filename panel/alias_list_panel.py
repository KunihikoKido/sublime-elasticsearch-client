import sublime


class AliasListPanel(object):

    def __init__(self, window, client, index=None):
        self.window = window
        self.client = client
        self.index = index
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        item = self.choices[index]
        self.callback(index=item[1], name=item[0])

    def show(self, callback):
        self.callback = callback

        options = dict(
            index=self.index
        )

        try:
            response = self.client.indices.get_alias(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices = []
        for index, aliases in response.items():
            for alias in aliases["aliases"].keys():
                self.choices.append([alias, index])

        self.choices.sort()

        self.window.show_quick_panel(self.choices, self.on_done)
