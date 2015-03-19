from .base import BaseElasticsearchCommand
from .base import make_path


class EsCatHealthCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatHealthCommand, self).run()

        url = make_path('_cat', 'health')
        params = {'v': 'true', 'ts': '0'}
        self.run_request('GET', url, None, params)


class EsCatShardsCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatShardsCommand, self).run()
        self.get_index(self.cat_shards)

    def cat_shards(self, index):
        url = make_path('_cat', 'shards', index)
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)


class EsCatIndexesCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatIndexesCommand, self).run()

        url = make_path('_cat', 'indices')
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)


class EsCatAliasesCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatAliasesCommand, self).run()
        self.get_alias(self.cat_aliases)

    def get_alias(self, callback):
        self.window.show_input_panel(
            'Alias: ', '', callback, None, None)

    def cat_aliases(self, alias):
        url = make_path('_cat', 'aliases', alias)
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)


class EsCatAllocationCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatAllocationCommand, self).run()
        url = make_path('_cat', 'allocation')
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)


class EsCatMasterCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatMasterCommand, self).run()
        url = make_path('_cat', 'master')
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)


class EsCatNodesCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatNodesCommand, self).run()
        url = make_path('_cat', 'nodes')
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)


class EsCatPenddingTasksCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatPenddingTasksCommand, self).run()
        url = make_path('_cat', 'pending_tasks')
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)


class EsCatPluginsCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatPluginsCommand, self).run()
        url = make_path('_cat', 'plugins')
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)


class EsCatRecoveryCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatRecoveryCommand, self).run()
        url = make_path('_cat', 'recovery')
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)


class EsCatThreadPoolCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatThreadPoolCommand, self).run()
        url = make_path('_cat', 'thread_pool')
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)


class EsCatSegmentsCommand(BaseElasticsearchCommand):

    def run(self):
        super(EsCatSegmentsCommand, self).run()
        url = make_path('_cat', 'segments')
        params = {'v': 'true'}
        self.run_request('GET', url, None, params)
