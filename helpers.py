import os.path
import glob
import datetime
import sublime
import sublime_plugin
import requests

from .base import ElasticsearchCommand

from elasticsearch import Elasticsearch
from elasticsearch.helpers import reindex
from elasticsearch.helpers import dumpdata
from elasticsearch.helpers import loaddata
from elasticsearch.helpers import copyindex


class HelperBaseCommand(ElasticsearchCommand):
    show_result_on_window = False
    syntax = 'Packages/JavaScript/JSON.tmLanguage'
    comfirm_message = None
    comfirm_ok_title = "OK"

    def is_comfirmed(self):
        ok = sublime.ok_cancel_dialog(
            "{}\n\nTarget: {}".format(
                self.comfirm_message, self.active_server),
            self.comfirm_ok_title)
        if ok:
            return True
        sublime.status_message('Canceled .')
        return False


class ReindexCommand(HelperBaseCommand):
    result_window_title = "Reindex"
    comfirm_message = 'Are you sure you want to reindex ?'
    comfirm_ok_title = 'Reindex'

    def run(self, chunk_size=1000):
        if not self.is_comfirmed():
            return

        self.request(reindex, self.esclient, source_index=self.index,
                     chunk_size=chunk_size, target_index=self.index)


class CopyIndexCommand(HelperBaseCommand):
    result_window_title = "Copy Index Data"
    comfirm_message = 'Are you sure you want to copy data ?'
    comfirm_ok_title = 'Copy'

    def source_esclient(self, index):
        s = self.servers[self.get_selected_server(index)]
        return Elasticsearch(s.get('base_url'), s.get('http_headers'))

    def source_index(self, index):
        s = self.servers[self.get_selected_server(index)]
        return s.get('index')

    def on_done(self, index):
        if index == -1:
            return

        if not self.is_comfirmed():
            return

        source_client = self.source_esclient(index)
        source_index = self.source_index(index)

        self.request(copyindex, source_client, source_index,
                     target_client=self.esclient, target_index=self.index,
                     chunk_size=self.chunk_size)

    def run(self, chunk_size=1000):
        self.chunk_size = chunk_size
        self.show_select_servers(self.on_done)


class DumpdataCommand(HelperBaseCommand):
    result_window_title = "Dump Data"
    comfirm_message = 'Are you sure you want to dump data ?'
    comfirm_ok_title = 'Dump data'

    @property
    def outputfile(self):
        now = datetime.datetime.now()
        filename = "dump-{0}-{1:%Y%m%d%H%M%S}.gz".format(self.index, now)
        return os.path.join(self.fixture_dir, filename)

    def is_enabled(self):
        return os.path.isdir(self.fixture_dir)

    def run(self, scroll='5m'):
        if not self.is_comfirmed():
            return

        self.request(dumpdata, self.outputfile,
                     self.esclient, self.index, scroll=scroll)


class LoaddataCommand(HelperBaseCommand):
    result_window_title = "Load Data"
    comfirm_message = 'Are you sure you want to load data ?'
    comfirm_ok_title = 'Load data'

    def is_enabled(self):
        return os.path.isdir(self.fixture_dir)

    @property
    def select_inputfiles(self):
        inputfiles = glob.glob(os.path.join(self.fixture_dir, 'dump-*.gz'))
        inputfiles = [os.path.basename(path) for path in inputfiles]
        inputfiles.sort(reverse=True)
        return inputfiles

    def show_select_inputfiles(self, callback):
        if not hasattr(self, '_selected_inputfile_index'):
            self._selected_inputfile_index = 0

        self.window.show_quick_panel(
            self.select_inputfiles, callback,
            selected_index=self._selected_inputfile_index)

    def get_selected_inputfile(self, index):
        self._selected_inputfile_index = index
        return os.path.join(self.fixture_dir, self.select_inputfiles[index])

    def on_done(self, index):
        if index == -1:
            return

        if not self.is_comfirmed():
            return

        inputfile = self.get_selected_inputfile(index)
        self.request(loaddata, inputfile, self.esclient, self.index)

    def run(self):
        self.show_select_inputfiles(self.on_done)


class CsvBulkIndexCommand(HelperBaseCommand):

    def run(self):
        self.window.run_command('csv_convert_bulk_format')
        self.window.run_command('bulk')


class SearchDocsCommand(sublime_plugin.WindowCommand):
    base_url = 'https://www.elastic.co'
    base_keywords = ['reference', 'elasticsearch']
    keywords = ''
    no_results_hits = [
        {
            'title': 'No results found...',
            'url': ''
        },
        {
            'title': 'Elasticsearch Reference | Elastic',
            'url': 'https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html'
        },
        {
            'title': 'Elasticsearch - The Definitive Guide | Elastic',
            'url': 'https://www.elastic.co/guide/en/elasticsearch/guide/current/index.html'
        },
        {
            'title': 'Hello Elasticsearch Blog (日本語) | by Kunihiko Kido',
            'url': 'https://medium.com/hello-elasticsearch'
        }
    ]

    @property
    def results_total(self):
        return self.results['total']

    @property
    def results_hits(self):
        return self.results['hits']

    @property
    def results_titles(self):
        hits = self.results_hits
        if self.is_no_results():
            hits = self.no_results_hits
        return [[hit['title'], hit['url']] for hit in hits]

    @property
    def results_urls(self):
        def make_url(url):
            if url.startswith('http') or not url:
                return url
            return self.base_url + url

        hits = self.results_hits
        if self.is_no_results():
            hits = self.no_results_hits
        return [make_url(hit['url']) for hit in hits]

    def query(self, keywords):
        self.keywords = keywords
        return ' '.join(self.base_keywords + keywords.split())

    def search(self, keywords):
        query = self.query(keywords)
        try:
            response = requests.get(
                'https://www.elastic.co/suggest',
                params={'q': query}, timeout=3, verify=False)

        except requests.exceptions.RequestException as e:
            return sublime.error_message("Error: {0!s}".format(e))

        self.results = response.json()
        self.window.show_quick_panel(self.results_titles, self.open_url)
        sublime.status_message('Total: {}'.format(self.results_total))

    def is_no_results(self):
        if self.results_total == 0:
            return True
        return False

    def open_url(self, index):
        if index == -1:
            return

        url = self.results_urls[index]

        if not url:
            return self.run()

        self.window.run_command('open_url', {'url': url})

    def run(self):
        self.window.show_input_panel(
            'Search in www.elastic.co:', self.keywords,
            self.search, None, None)
