from .base import ElasticsearchCommand

DEFAULT_PARAMS = dict(v=1)


class CatClientCommand(ElasticsearchCommand):
    show_result_on_window = True
    syntax = 'Packages/Text/Plain text.tmLanguage'
    result_window_title = ""

    def request_cat_api(self, method_name, *args, **kwargs):
        method = getattr(self.esclient.cat, method_name)
        kwargs = kwargs or {}
        kwargs['params'] = DEFAULT_PARAMS
        self.request(method, *args, **kwargs)


class CatAliasesCommand(CatClientCommand):
    result_window_title = "Cat Aliases"

    def run(self):
        self.get_alias(self.on_done)

    def on_done(self, name):
        self.request_cat_api('aliases', name=name)


class CatAllocationCommand(CatClientCommand):
    result_window_title = "Cat Allocation"

    def run(self):
        self.get_node_id(self.on_done)

    def on_done(self, node_id):
        self.request_cat_api('allocation', node_id=node_id)


class CatCountCommand(CatClientCommand):
    result_window_title = "Cat Count"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_cat_api('count', index=index)


class CatHealthCommand(CatClientCommand):
    result_window_title = "Cat Health"

    def run(self):
        self.request_cat_api('health')


class CatHelpCommand(CatClientCommand):
    result_window_title = "Cat Help"

    def run(self):
        self.request_cat_api('help')


class CatIndicesCommand(CatClientCommand):
    result_window_title = "Cat Indices"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_cat_api('indices', index=index)


class CatMasterCommand(CatClientCommand):
    result_window_title = "Cat Master"

    def run(self):
        self.request_cat_api('master')


class CatNodesCommand(CatClientCommand):
    result_window_title = "Cat Nodes"

    def run(self):
        self.request_cat_api('nodes')


class CatRecoveryCommand(CatClientCommand):
    result_window_title = "Cat Recovery"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_cat_api('recovery', index=index)


class CatShardsCommand(CatClientCommand):
    result_window_title = "Cat Shards"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_cat_api('shards', index=index)


class CatSegmentsCommand(CatClientCommand):
    result_window_title = "Cat Segments"

    def run(self):
        self.get_index(self.on_done)

    def on_done(self, index):
        self.request_cat_api('segments', index=index)


class CatPendingTasksCommand(CatClientCommand):
    result_window_title = "Cat Pending Tasks"

    def run(self):
        self.request_cat_api('pending_tasks')


class CatThreadPoolCommand(CatClientCommand):
    result_window_title = "Cat Thread Pool"

    def run(self):
        self.request_cat_api('thread_pool')


class CatFielddataCommand(CatClientCommand):
    result_window_title = "Cat Fielddata"

    def run(self, fields=None):
        self.get_fields(self.on_done)

    def on_done(self, fields):
        self.request_cat_api('fielddata', fields=fields)


class CatPluginsCommand(CatClientCommand):
    result_window_title = "Cat Plugins"

    def run(self):
        self.request_cat_api('plugins')
