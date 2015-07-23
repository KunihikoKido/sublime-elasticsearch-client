import sublime


class IndexTemplateListPanel(object):

    def __init__(self, window, client):
        self.window = window
        self.client = client
        self.choices = []

    def on_done(self, index):
        if index == -1:
            return
        name = self.choices[index]
        self.callback(name=name)

    def show(self, callback):
        self.callback = callback

        options = dict()

        try:
            response = self.client.indices.get_template(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        self.choices = []
        for name in response.keys():
            self.choices.append(name)
        self.choices.sort()
        self.window.show_quick_panel(self.choices, self.on_done)
