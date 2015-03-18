from .base import BaseElasticsearchCommand
from .base import make_path
from .base import DEFAULT_PARAMS

__all__ = ["EsCreateIndexCommand", "EsDeleteIndexCommand",
           "EsGetIndexSettingsCommand", "EsPutMappingCommand",
           "EsGetMappingCommand", "EsDeleteMappingCommand",
           "EsAnalyzeCommand"]


class EsCreateIndexCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCreateIndexCommand, self).run()

        if not self.enabled_create_index:
            self.status_message('*** Disabled Create Index! ***')
            return

        self.get_index(self.create_index)

    def create_index(self, index):
        if not index:
            self.status_message('Canceled')
            return

        url = make_path(index)
        self.run_request('PUT', url)
        self.set_index(index)


class EsDeleteIndexCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsDeleteIndexCommand, self).run()

        if not self.enabled_delete_index:
            self.status_message('*** Disabled Delete Index! ***')
            return

        self.get_index(self.delete_index)

    def delete_index(self, index):
        if not index:
            self.status_message('Canceled')
            return

        url = make_path(index)
        self.run_request('DELETE', url)


class EsGetIndexSettingsCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsGetIndexSettingsCommand, self).run()

        self.get_index(self.get_index_settings)

    def get_index_settings(self, index):
        if not index:
            self.status_message('Canceled')
            return

        url = make_path(index, '_settings')
        self.run_request('GET', url)
        self.set_index(index)


class EsPutMappingCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsPutMappingCommand, self).run()

        if not self.enabled_put_mapping:
            self.status_message('*** Disabled Put Mapping! ***')
            return

        if not self.index:
            self.get_index(self.set_index)
            return

        self.get_doc_type(self.put_mapping)

    def set_index(self, index):
        super(EsPutMappingCommand, self).set_index(index)
        self.run()

    def put_mapping(self, doc_type):
        if not doc_type:
            self.status_message('Canceled')
            return

        url = make_path(self.index, '_mapping', doc_type)
        body = self.get_selection_text()
        self.run_request('PUT', url, body)

        self.set_doc_type(doc_type)


class EsGetMappingCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsGetMappingCommand, self).run()

        if not self.index:
            self.get_index(self.set_index)
            return

        self.get_doc_type(self.get_mapping)

    def set_index(self, index):
        super(EsGetMappingCommand, self).set_index(index)
        self.run()

    def get_mapping(self, doc_type):
        if not doc_type:
            self.status_message('Canceled')
            return

        url = make_path(self.index, '_mapping', doc_type)
        self.run_request('GET', url)

        self.set_doc_type(doc_type)


class EsDeleteMappingCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsDeleteMappingCommand, self).run()

        if not self.enabled_delete_mapping:
            self.status_message('*** Disabled Delete Mapping! ***')
            return

        if not self.index:
            self.get_index(self.set_index)
            return

        self.get_doc_type(self.delete_mapping)

    def set_index(self, index):
        super(EsDeleteMappingCommand, self).set_index(index)
        self.run()

    def delete_mapping(self, doc_type):
        if not doc_type:
            self.status_message('Canceled')
            return

        url = make_path(self.index, doc_type)
        self.run_request('DELETE', url)

        self.set_doc_type(doc_type)


class EsAnalyzeCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsAnalyzeCommand, self).run()

        if not self.index:
            self.get_index(self.set_index)
            return

        self.get_analyzer(self.analyze)

    def set_index(self, index):
        super(EsAnalyzeCommand, self).set_index(index)
        self.run()

    def analyze(self, analyzer):
        if not analyzer:
            self.status_message('canceled')
            return

        url = make_path(self.index, '_analyze')
        body = self.get_selection_text()
        params = {'analyzer': analyzer}
        params.update(DEFAULT_PARAMS)
        self.run_request('POST', url, body, params)

        self.set_analyzer(analyzer)
