from .base import ElasticsearchCommand


class NodesInfoCommand(ElasticsearchCommand):
    result_window_title = "Nodes Info"

    def run(self):
        self.get_node_id(self.on_done)

    def on_done(self, node_id):
        self.request(self.esclient.nodes.info, node_id=node_id)


class NodesShutdownCommand(ElasticsearchCommand):
    result_window_title = "Nodes Shutdown"

    def run(self):
        self.get_node_id(self.on_done)

    def on_done(self, node_id):
        self.request(self.esclient.nodes.shutdown, node_id=node_id)


class NodesStatsCommand(ElasticsearchCommand):
    result_window_title = "Nodes Stats"

    def run(self):
        self.get_node_id(self.on_done)

    def on_done(self, node_id):
        self.request(self.esclient.nodes.stats, node_id=node_id)


class NodesHotThreadsCommand(ElasticsearchCommand):
    result_window_title = "Nodes hot_threads"

    def run(self):
        self.get_node_id(self.on_done)

    def on_done(self, node_id):
        self.request(self.esclient.nodes.hot_threads, node_id=node_id)
