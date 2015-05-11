import os.path
import glob
import datetime
import sublime

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

    @property
    def select_items(self):
        items = list(self.servers.keys())
        items.sort(reverse=True)
        return items

    def show_select_items(self, callback):
        self.window.show_quick_panel(self.select_items, callback)

    def run(self, chunk_size=1000):
        self.chunk_size = chunk_size
        self.show_select_items(self.on_done)

    def source_esclient(self, index):
        s = self.servers[self.select_items[index]]
        return Elasticsearch(s.get('base_url'), s.get('http_headers'))

    def source_index(self, index):
        s = self.servers[self.select_items[index]]
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
    def select_items(self):
        items = glob.glob(os.path.join(self.fixture_dir, 'dump-*.gz'))
        items.sort(reverse=True)
        return items

    def show_select_items(self, callback):
        self.window.show_quick_panel(self.select_items, callback)

    def run(self):
        self.show_select_items(self.on_done)

    def on_done(self, index):
        if index == -1:
            return

        if not self.is_comfirmed():
            return

        inputfile = self.select_items[index]
        self.request(loaddata, inputfile, self.esclient, self.index)
