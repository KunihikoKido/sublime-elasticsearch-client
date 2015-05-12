from .base import ElasticsearchCommand


class NodesClientCommand(ElasticsearchCommand):
    def request_nodes_api(self, method, *args, **kwargs):
        method = getattr(self.esclient.nodes, method.lower())
        kwargs = kwargs or {}
        self.request(method, *args, **kwargs)


class NodesInfoCommand(NodesClientCommand):
    result_window_title = "Nodes Info"

    def run(self):
        self.get_node_id(self.on_done)

    def on_done(self, node_id):
        self.request_nodes_api('info', node_id=node_id)


class NodesShutdownCommand(NodesClientCommand):
    result_window_title = "Nodes Shutdown"

    def run(self):
        self.get_node_id(self.on_done)

    def on_done(self, node_id):
        self.request_nodes_api('shutdown', node_id=node_id)


class NodesStatsCommand(NodesClientCommand):
    result_window_title = "Nodes Stats"

    def run(self):
        self.get_node_id(self.on_done)

    def on_done(self, node_id):
        self.request_nodes_api('stats', node_id=node_id)


class NodesHotThreadsCommand(NodesClientCommand):
    result_window_title = "Nodes hot_threads"

    def run(self):
        self.get_node_id(self.on_done)

    def on_done(self, node_id):
        self.request_nodes_api('hot_threads', node_id=node_id)
