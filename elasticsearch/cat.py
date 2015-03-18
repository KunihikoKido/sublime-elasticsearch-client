from .base import BaseElasticsearchCommand
from .base import make_path

__all__ = ["EsCatHealthCommand", "EsCatShardsCommand",
           "EsCatIndexesCommand"]


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
