import tempfile
from .base import ElasticsearchCommand
from elasticsearch.utils import make_url
from elasticsearch.utils import make_path


class ApacheBenchCommand(ElasticsearchCommand):
    selected_index = 0

    def run(self):
        self.select_panel(self.on_done)

    def make_postfile(self):
        file_name = self.window.active_view().file_name()
        if not file_name:
            selection = self.selection()
            temp = tempfile.NamedTemporaryFile(delete=False)
            temp.write(bytes(selection, 'utf-8'))
            file_name = temp.name
            temp.close()
        return file_name

    def select_panel(self, callback):
        ab_options = list(self.ab_options.keys())
        ab_options.sort()
        self.window.show_quick_panel(
            ab_options, callback, selected_index=self.selected_index)

    def apache_bench(self, path, ab_options, postfile):
        url = make_url(self.base_url, path)
        command = [self.ab_command]
        command += ab_options

        for k, v in self.http_headers.items():
            command += ['-H', "{0}: {1}".format(k, v)]

        command += ['-p', postfile]
        command += [url]
        self.window.run_command('exec', {'cmd': command})

    def make_path(self):
        return make_path(self.index, self.doc_type, '_search')

    def get_ab_options(self, index):
        ab_options = list(self.ab_options.keys())
        ab_options.sort()
        selected = ab_options[index]
        return self.ab_options[selected]

    def on_done(self, index):
        if index == -1:
            return

        self.selected_index = index

        ab_options = self.get_ab_options(index)
        path = self.make_path()
        postfile = self.make_postfile()
        self.apache_bench(path, ab_options, postfile)


class ApacheBenchForSearchTemplateCommand(ApacheBenchCommand):
    """ Apache Bentch for Search Template Query """

    def make_path(self):
        return make_path(self.index, self.doc_type, '_search', 'template')
