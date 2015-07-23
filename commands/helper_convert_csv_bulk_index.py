import sublime
import sublime_plugin
import csv
import io
import json


class HelperConvertCsvBulkIndexCommand(sublime_plugin.TextCommand):

    def is_enabled(self):
        return True

    def new_file(self, title=''):
        view = sublime.active_window().new_file()
        view.set_name('**Bulk {} Data**'.format(title))
        view.set_scratch(True)
        view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')
        return view

    def run(self, edit, action='index'):

        text = self.view.substr(sublime.Region(0, self.view.size()))

        output_view = self.new_file(action)

        for doc in csv.DictReader(io.StringIO(text.strip())):
            bulk_action = {action: {}}

            if 'id' in doc:
                bulk_action[action]['_id'] = doc['id']

            data = []
            data.append(json.dumps(bulk_action))

            if action in ('index', 'create'):
                data.append(json.dumps(doc, ensure_ascii=False))
            elif action == 'update':
                data.append(json.dumps({'doc': doc}, ensure_ascii=False))

            output_text = '\n'.join(data) + '\n'

            output_view.insert(
                edit, output_view.size(), output_text)
