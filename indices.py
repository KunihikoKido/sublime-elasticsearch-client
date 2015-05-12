from .base import ElasticsearchCommand
from .base import delete_ok_cancel_dialog


class IndicesClientCommand(ElasticsearchCommand):

    def request_indices_api(self, method, *args, **kwargs):
        method = getattr(self.esclient.indices, method.lower())
        self.request(method, *args, **kwargs)


class AnalyzeTextCommand(IndicesClientCommand):
    result_window_title = "Analyze Text"

    def run(self):
        self.get_analyzer(self.on_done)

    def on_done(self, analyzer):
        self.request_indices_api(
            'analyze', index=self.index, doc_type=self.doc_type,
            body=self.selection(), params=dict(analyzer=analyzer))


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
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_indices_api('create', index=index)


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
        self.request_indices_api('put_settings', body=self.selection())


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
