import json
import sublime
from .utils import show_result_json


def scan(client, query=None, scroll='5m', **kwargs):

    kwargs['params'] = dict(search_type='scan', scroll=scroll)

    result = client.search(body=query, **kwargs)
    scroll_id = result.get('_scroll_id')
    if not scroll_id:
        return

    params = dict(scroll=scroll)

    while True:
        result = client.scroll(scroll_id, params=params)

        if not result['hits']['hits']:
            break

        for hit in result['hits']['hits']:
            yield hit

        scroll_id = result.get('_scroll_id')

        if not scroll_id:
            break


def reindex(client, source_index, target_index, query=None, target_client=None,
            scroll='5m', scan_kwargs={}, command=None):

    target_client = client if target_client is None else target_client

    docs = scan(client, query=query, index=source_index,
                scroll=scroll, **scan_kwargs)

    count = 0
    for doc in docs:
        target_client.index(index=target_index, doc_type=doc['_type'],
                            body=json.dumps(doc['_source']), id=doc['_id'])
        count += 1
        sublime.status_message("{0:_>10}".format(count))

    result = {
        "_source": {
            "host": client.base_url,
            "index": source_index
        },
        "_target": {
            "host": target_client.base_url,
            "index": target_index
        },
        "docs": count
    }

    show_result_json(result, sort_keys=True, command=command)
