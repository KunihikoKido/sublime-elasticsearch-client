import json
import sublime
from .utils import show_result_json
from .utils import make_url


def scan(client, query=None, scroll='5m', **kwargs):

    kwargs['params'] = dict(search_type='scan', scroll=scroll)

    result = client.search(body=query, **kwargs)
    scroll_id = result.get('_scroll_id')
    if not scroll_id:
        return

    params = dict(scroll=scroll)

    while True:
        result = client.scroll(scroll_id, params=params)

        if 'error' in result.keys():
            import sys
            sublime.error_message("Error: {}".format(result['error']))
            sys.exit(1)

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

    result = {
        "_source": make_url(client.base_url, source_index),
        "_target": make_url(target_client.base_url, target_index),
    }

    docs = scan(client, query=query, index=source_index,
                scroll=scroll, **scan_kwargs)

    success, failed = 0, 0

    for doc in docs:
        response = target_client.index(
            index=target_index, doc_type=doc['_type'],
            body=json.dumps(doc['_source']), id=doc['_id'])

        if 'error' in response.keys():
            failed += 1
        else:
            success += 1

        sublime.status_message("{0:_>10}".format(success + failed))

    result['success'] = success
    result['failed'] = failed

    show_result_json(result, sort_keys=True, command=command)
