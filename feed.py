import sublime_plugin

import xml.etree.ElementTree as etree
from urllib.request import urlopen


class ElementWrapper:
    def __init__(self, element):
        self._element = element

    def __getattr__(self, tag):
        if tag.startswith("__"):
            raise AttributeError(tag)
        return self._element.findtext(tag)


class FeedCommand(sublime_plugin.WindowCommand):

    @property
    def items(self):
        items = []
        tree = etree.parse(urlopen(self.url))
        for item in tree.findall('.//item'):
            items.append(ElementWrapper(item))
        return items

    @property
    def item_titles(self):
        return [[item.title, item.pubDate] for item in self.items]

    @property
    def item_links(self):
        return [item.link for item in self.items]

    def run(self, url=None):
        self.url = url
        self.window.show_quick_panel(self.item_titles, self.open_url)

    def open_url(self, index):
        if index == -1:
            return

        url = self.item_links[index]

        if not url:
            return self.run()

        self.window.run_command('open_url', {'url': url})
