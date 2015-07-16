import sublime_plugin


class ShowResponseCommand(sublime_plugin.WindowCommand):
    default_syntax = 'Packages/JavaScript/JSON.tmLanguage'

    def run(self, title="", text=""):
        panel = self.window.new_file()
        panel.set_name('{}'.format(title))
        panel.set_scratch(True)
        panel.set_syntax_file(self.default_syntax)
        panel.set_scratch(True)
        panel.set_read_only(False)
        panel.settings().set('gutter', True)
        panel.settings().set('line_numbers', True)
        panel.settings().set('word_wrap', False)
        panel.run_command('append', {'characters': text})
        panel.set_read_only(True)
