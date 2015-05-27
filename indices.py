from .base import ElasticsearchCommand
from .base import delete_ok_cancel_dialog
from elasticsearch.helpers import analyze_keywords


class IndicesClientCommand(ElasticsearchCommand):

    def request_indices_api(self, method, *args, **kwargs):
        method = getattr(self.esclient.indices, method.lower())
        self.request(method, *args, **kwargs)


class AnalyzeTextCommand(IndicesClientCommand):
    result_window_title = "Analyze Text"
    default_analyzers = [
        'Standard Analyzer: standard',
        'Simple Analyzer: simple',
        'Whitespace Analyzer: whitespace',
        'Stop Analyzer: stop',
        'Keyword Analyzer: keyword',
        'Pattern Analyzer: pattern',
        'Snowball Analyzer: snowball',
        'Language Analyzer: arabic',
        'Language Analyzer: armenian',
        'Language Analyzer: basque',
        'Language Analyzer: brazilian',
        'Language Analyzer: bulgarian',
        'Language Analyzer: catalan',
        'Language Analyzer: chinese',
        'Language Analyzer: cjk',
        'Language Analyzer: czech',
        'Language Analyzer: danish',
        'Language Analyzer: dutch',
        'Language Analyzer: english',
        'Language Analyzer: finnish',
        'Language Analyzer: french',
        'Language Analyzer: galician',
        'Language Analyzer: german',
        'Language Analyzer: greek',
        'Language Analyzer: hindi',
        'Language Analyzer: hungarian',
        'Language Analyzer: indonesian',
        'Language Analyzer: irish',
        'Language Analyzer: italian',
        'Language Analyzer: latvian',
        'Language Analyzer: norwegian',
        'Language Analyzer: persian',
        'Language Analyzer: portuguese',
        'Language Analyzer: romanian',
        'Language Analyzer: russian',
        'Language Analyzer: sorani',
        'Language Analyzer: spanish',
        'Language Analyzer: swedish',
        'Language Analyzer: turkish',
        'Language Analyzer: thai',
    ]

    @property
    def custom_analyzers(self):
        r = self.esclient.indices.get_settings(index=self.index)
        items = list(r[self.index]['settings']['index']['analysis']['analyzer'].keys())
        return list(map(lambda s: "Custom Analyzer: {}".format(s), items))

    @property
    def select_analyzers(self):
        analyzers = self.default_analyzers + self.custom_analyzers
        analyzers.sort(reverse=False)
        return analyzers

    def show_select_analyzers(self, callback):
        if not hasattr(self, '_selected_analyzer_index'):
            self._selected_analyzer_index = 0

        self.window.show_quick_panel(
            self.select_analyzers, callback,
            selected_index=self._selected_analyzer_index)

    def get_selected_analyzer(self, index):
        self._selected_analyzer_index = index
        return self.select_analyzers[index].split()[-1]

    def run(self):
        self.show_select_analyzers(self.on_done)

    def on_done(self, index):
        if index == -1:
            return

        analyzer = self.get_selected_analyzer(index)

        self.request_indices_api(
            'analyze', index=self.index,
            body=self.selection(), params=dict(analyzer=analyzer))


class AnalyzeKeywordsCommand(AnalyzeTextCommand):

    def on_done(self, index):
        if index == -1:
            return

        analyzer = self.get_selected_analyzer(index)

        analyze_keywords(
            self.esclient, index=self.index,
            body=self.selection(), analyzer=analyzer, command=self)


class RefreshIndexCommand(IndicesClientCommand):
    result_window_title = "Refresh Index"

    def run(self):
        self.request_indices_api('refresh', index=self.index)


class FlushIndexCommand(IndicesClientCommand):
    result_window_title = "Flush Index"

    def run(self):
        self.request_indices_api('flush', index=self.index)


class CreateIndexCommand(IndicesClientCommand):
    result_window_title = "Create Index"

    def run(self):
        self.get_index(self.first_done)

    def first_done(self, text):
        self._index = text
        self.get_shards(self.second_done)

    def second_done(self, text):
        self._shards = text
        self.get_replicas(self.third_done)

    def third_done(self, text):
        self._replicas = text
        self.create_index()

    def create_index(self):
        body = dict(settings=dict(
            number_of_shards=self._shards,
            number_of_replicas=self._replicas))

        self.request_indices_api('create', index=self._index, body=body)


class GetIndexInfomationCommand(IndicesClientCommand):
    result_window_title = "Get Index Infomation"

    def run(self):
        self.get_include_feature(self.on_done)

    def on_done(self, feature):
        self.request_indices_api('get', index=self.index, feature=feature)


class OpenIndexCommand(IndicesClientCommand):
    result_window_title = "Open Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('open', index=index)


class CloseIndexCommand(IndicesClientCommand):
    result_window_title = "Close Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('close', index=index)


class DeleteIndexCommand(IndicesClientCommand):
    result_window_title = "Delete Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        if not delete_ok_cancel_dialog(index):
            return

        self.request_indices_api('delete', index=self.index)


class PutMappingCommand(IndicesClientCommand):
    result_window_title = "Put Mapping"

    def run(self):
        self.request_indices_api(
            'put_mapping', index=self.index, doc_type=self.doc_type,
            body=self.selection())


class GetMappingCommand(IndicesClientCommand):
    result_window_title = "Get Mapping"

    def run(self):
        self.request_indices_api(
            'get_mapping', index=self.index, doc_type=self.doc_type)


class GetFieldMappingCommand(IndicesClientCommand):
    result_window_title = "Get Field Mapping"

    def run(self):
        self.get_field(self.on_done)

    def on_done(self, field):
        self.request_indices_api(
            'get_field_mapping', index=self.index,
            doc_type=self.doc_type, field=field)


class DeleteMappingCommand(IndicesClientCommand):
    result_window_title = "Delete Mapping"

    def run(self):
        if not delete_ok_cancel_dialog(self.doc_type):
            return

        self.request_indices_api(
            'delete_mapping', index=self.index, doc_type=self.doc_type)


class PutIndexAliasCommand(IndicesClientCommand):
    result_window_title = "Put Index Alias"

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, name):
        self.request_indices_api('put_alias', index=self.index, name=name)


class GetIndexAliasCommand(IndicesClientCommand):
    result_window_title = "Get Index Alias"

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, name):
        self.request_indices_api('get_alias', index=self.index, name=name)


class UpdateIndexAliasesCommand(IndicesClientCommand):
    result_window_title = "Update Index Aliases"

    def run(self):
        self.request_indices_api('update_aliases', body=self.selection())


class DeleteIndexAliasCommand(IndicesClientCommand):
    result_window_title = "Delete Index Alias"

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, name):
        if not delete_ok_cancel_dialog(name):
            return

        self.request_indices_api('delete_alias', index=self.index, name=name)


class PutIndexTemplateCommand(IndicesClientCommand):
    result_window_title = "Put Index Template"

    def run(self):
        self.get_index_template(self.on_done)

    def on_done(self, name):
        self.request_indices_api(
            'put_template', name=name, body=self.selection())


class GetIndexTemplateCommand(PutIndexTemplateCommand):
    result_window_title = "Get Index Template"

    def on_done(self, name):
        self.request_indices_api('get_template', name=name)


class DeleteIndexTemplateCommand(PutIndexTemplateCommand):
    result_window_title = "Delete Index Template"

    def on_done(self, name):
        if not delete_ok_cancel_dialog(name):
            return

        self.request_indices_api('delete_template', name=name)


class GetIndexSettingsCommand(IndicesClientCommand):
    result_window_title = "Get Index Settings"

    def run(self):
        self.request_indices_api('get_settings', index=self.index)


class PutIndexSettingsCommand(IndicesClientCommand):
    result_window_title = "Put Index Settings"

    def run(self):
        self.request_indices_api(
            'put_settings', index=self.index, body=self.selection())


class ChangeReplicasCommand(IndicesClientCommand):
    result_window_title = "Change Number Of Replicas"

    def get_index_settings(self):
        return self.esclient.indices.get_settings(index=self.index)

    def is_enabled(self):
        if self.index in self.get_index_settings().keys():
            return True
        return False

    def number_of_replicas(self):
        r = self.esclient.indices.get_settings(index=self.index)
        return r[self.index]['settings']['index']['number_of_replicas']

    def run(self):
        self.get_replicas(self.on_done, default=self.number_of_replicas())

    def on_done(self, replicas):
        body = dict(index=dict(number_of_replicas=replicas))
        self.request_indices_api(
            'put_settings', index=self.index, body=body)


class PutIndexWarmerCommand(IndicesClientCommand):
    result_window_title = "Put Index Warmer"

    def run(self):
        self.get_warmer(self.on_done)

    def on_done(self, name):
        self.request_indices_api(
            'put_warmer', index=self.index,
            name=name, body=self.selection())


class GetIndexWarmerCommand(PutIndexWarmerCommand):
    result_window_title = "Get Index Warmer"

    def on_done(self, name):
        self.request_indices_api('get_warmer', index=self.index, name=name)


class DeleteIndexWarmerCommand(PutIndexWarmerCommand):
    result_window_title = "Delete Index Warmer"

    def on_done(self, name):
        if not delete_ok_cancel_dialog(name):
            return

        self.request_indices_api('delete_warmer', index=self.index, name=name)


class IndexStatusCommand(IndicesClientCommand):
    result_window_title = "Index Status"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('status', index=index)


class IndexStatsCommand(IndicesClientCommand):
    result_window_title = "Index Stats"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('stats', index=index)


class IndexSegmentsInfomationCommand(IndicesClientCommand):
    result_window_title = "Index Segments Infomation"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('segments', index=index)


class OptimizeIndexCommand(IndicesClientCommand):
    result_window_title = "Optimize Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('optimize', index=index)


class ClearIndexCacheCommand(IndicesClientCommand):
    result_window_title = "Clear Index Cache"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('clear_cache', index=index)


class IndexRecoveryStatusCommand(IndicesClientCommand):
    result_window_title = "Index Recovery Status"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('recovery', index=index)


class UpgradeIndexCommand(IndicesClientCommand):
    result_window_title = "Upgrade Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('upgrade', index=index)


class GetUpgradeIndexStatus(IndicesClientCommand):
    result_window_title = "Get Upgrade Index Status"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('get_upgrade', index=index)
