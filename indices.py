from .base import ESClientBaseCommand
from .base import delete_ok_cancel_dialog


class AnalyzeTextCommand(ESClientBaseCommand):
    result_window_title = "Analyze Text"

    def run(self):
        self.get_analyzer(self.on_done)

    def on_done(self, analyzer):
        es = self.ESClient()
        params = dict(analyzer=analyzer)
        body = self.selection()
        self.request(es.indices.analyze, self.index, body, params)


class RefreshIndexCommand(ESClientBaseCommand):
    result_window_title = "Refresh Index"

    def run(self, index):
        es = self.ESClient()
        self.request(es.indices.refresh, self.index)


class FlushIndexCommand(ESClientBaseCommand):
    result_window_title = "Flush Index"

    def run(self):
        es = self.ESClient()
        self.request(es.indices.flush, self.index)


class CreateIndexCommand(ESClientBaseCommand):
    result_window_title = "Create Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        if not index:
            return

        es = self.ESClient()
        self.request(es.indices.create, index)


class GetIndexInfomationCommand(ESClientBaseCommand):
    result_window_title = "Get Index Infomation"

    def run(self):
        self.get_include_feature(self.on_done)

    def on_done(self, feature):
        es = self.ESClient()
        self.request(es.indices.get, self.index, feature)


class OpenIndexCommand(ESClientBaseCommand):
    result_window_title = "Open Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        if not index:
            return

        es = self.ESClient()
        self.request(es.indices.open, index)


class CloseIndexCommand(ESClientBaseCommand):
    result_window_title = "Close Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        if not index:
            return

        es = self.ESClient()
        self.request(es.indices.close, index)


class DeleteIndexCommand(ESClientBaseCommand):
    result_window_title = "Delete Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        if not index:
            return

        if not delete_ok_cancel_dialog(index):
            return

        es = self.ESClient()
        self.request(es.indices.delete, index)


class PutMappingCommand(ESClientBaseCommand):
    result_window_title = "Put Mapping"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(
            es.indices.put_mapping, self.index, self.doc_type, body)


class GetMappingCommand(ESClientBaseCommand):
    result_window_title = "Get Mapping"

    def run(self):
        es = self.ESClient()
        self.request(
            es.indices.get_mapping, self.index, self.doc_type)


class GetFieldMappingCommand(ESClientBaseCommand):
    result_window_title = "Get Field Mapping"

    def run(self):
        self.get_field(self.on_done)

    def on_done(self, field):
        if not field:
            return

        es = self.ESClient()
        self.request(
            es.indices.get_field_mapping, self.index, self.doc_type, field)


class DeleteMappingCommand(ESClientBaseCommand):
    result_window_title = "Delete Mapping"

    def run(self):
        if not delete_ok_cancel_dialog(self.doc_type):
            return

        es = self.ESClient()
        self.request(
            es.indices.delete_mapping, self.index, self.doc_type)


class PutIndexAliasCommand(ESClientBaseCommand):
    result_window_title = "Put Index Alias"

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, name):
        if not name:
            return

        es = self.ESClient()
        self.request(es.indices.put_alias, self.index, name)


class GetIndexAliasCommand(ESClientBaseCommand):
    result_window_title = "Get Index Alias"

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, name):
        es = self.ESClient()
        self.request(es.indices.get_alias, self.index, name)


class UpdateIndexAliasesCommand(ESClientBaseCommand):
    result_window_title = "Update Index Aliases"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.indices.update_aliases, body)


class DeleteIndexAliasCommand(ESClientBaseCommand):
    result_window_title = "Delete Index Alias"

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, name):
        if not delete_ok_cancel_dialog(name):
            return

        es = self.ESClient()
        self.request(es.indices.delete_alias, self.index, name)


class PutIndexTemplateCommand(ESClientBaseCommand):
    result_window_title = "Put Index Template"

    def run(self):
        self.get_index_template(self.on_done)

    def on_done(self, name):
        if not name:
            return

        es = self.ESClient()
        body = self.selectio()
        self.request(es.indices.put_template, name, body)


class GetIndexTemplateCommand(PutIndexTemplateCommand):
    result_window_title = "Get Index Template"

    def on_done(self, name):
        es = self.ESClient()
        self.request(es.indices.get_template, name)


class DeleteIndexTemplateCommand(PutIndexTemplateCommand):
    result_window_title = "Delete Index Template"

    def on_done(self, name):
        if not name:
            return

        if not delete_ok_cancel_dialog(name):
            return

        es = self.ESClient()
        self.request(es.indices.delete_template, name)


class GetIndexSettingsCommand(ESClientBaseCommand):
    result_window_title = "Get Index Settings"

    def run(self):
        es = self.ESClient()
        self.request(es.indices.get_settings, self.index, None)


class PutIndexSettingsCommand(ESClientBaseCommand):
    result_window_title = "Put Index Settings"

    def run(self):
        es = self.ESClient()
        body = self.selection()
        self.request(es.indices.put_settings, body)


class PutIndexWarmerCommand(ESClientBaseCommand):
    result_window_title = "Put Index Warmer"

    def run(self):
        self.get_warmer(self.on_done)

    def on_done(self, name):
        if not name:
            return

        es = self.ESClient()
        body = self.selection()
        self.request(es.indices.put_warmer, self.index, name, body)


class GetIndexWarmerCommand(PutIndexWarmerCommand):
    result_window_title = "Get Index Warmer"

    def on_done(self, name):
        es = self.ESClient()
        self.request(es.indices.get_warmer, self.index, name)


class DeleteIndexWarmerCommand(PutIndexWarmerCommand):
    result_window_title = "Delete Index Warmer"

    def on_done(self, name):
        es = self.ESClient()
        self.request(es.indices.delete_warmer, self.index, name)


class IndexStatusCommand(ESClientBaseCommand):
    result_window_title = "Index Status"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        es = self.ESClient()
        self.request(es.indices.status, index)


class IndexStatsCommand(ESClientBaseCommand):
    result_window_title = "Index Stats"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        es = self.ESClient()
        self.request(es.indices.stats, index)


class IndexSegmentsInfomationCommand(ESClientBaseCommand):
    result_window_title = "Index Segments Infomation"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        es = self.ESClient()
        self.request(es.indices.segments, index)


class OptimizeIndexCommand(ESClientBaseCommand):
    result_window_title = "Optimize Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        es = self.ESClient()
        self.request(es.indices.optimize, index)


class ClearIndexCacheCommand(ESClientBaseCommand):
    result_window_title = "Clear Index Cache"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        es = self.ESClient()
        self.request(es.indices.clear_cache, index)


class IndexRecoveryStatusCommand(ESClientBaseCommand):
    result_window_title = "Index Recovery Status"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        es = self.ESClient()
        self.request(es.indices.recovery, index)


class UpgradeIndexCommand(ESClientBaseCommand):
    result_window_title = "Upgrade Index"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        es = self.ESClient()
        self.request(es.indices.upgrade, index)


class GetUpgradeIndexStatus(ESClientBaseCommand):
    result_window_title = "Get Upgrade Index Status"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        es = self.ESClient()
        self.request(es.indices.get_upgrade, index)
