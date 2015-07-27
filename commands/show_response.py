import sublime_plugin


class ShowResponseCommand(sublime_plugin.WindowCommand):
    default_syntax = 'Packages/JavaScript/JSON.tmLanguage'

    def run(self, title="", text=""):
        request_view = self.window.active_view()
        request_view_group, request_view_index = \
            self.window.get_view_index(request_view)

        self.window.run_command('set_layout', {
            'cols':  [0.0, 0.5, 1.0],
            'rows':  [0.0, 1.0],
            'cells': [[0, 0, 1, 1], [1, 0, 2, 1]]
         })

        self.window.set_view_index(
            request_view, request_view_group,
            request_view_index)

        self.window.focus_group(1)

        panel = self.window.new_file()
        panel.set_name('RESPONSE: {}'.format(title))
        panel.set_scratch(True)
        panel.set_syntax_file(self.default_syntax)
        panel.set_scratch(True)
        panel.set_read_only(False)
        panel.settings().set('gutter', True)
        panel.settings().set('line_numbers', True)
        panel.settings().set('word_wrap', False)
        panel.run_command('append', {'characters': text})
        panel.set_read_only(True)

        views = self.window.views_in_group(self.window.active_group())
        for view in views:
            if panel.id() != view.id() and request_view.id() != view.id():
                self.window.focus_view(view)
                self.window.run_command("close_file")

        self.window.focus_group(request_view_group)
        self.window.focus_view(request_view)
