import gzip
import json
import sublime
from itertools import islice
from operator import methodcaller

from .utils import show_result_json
from .utils import make_url


def change_index(hits, index):
    for hit in hits:
        hit['_index'] = index
        yield hit


def expand_action(data):
    data = data.copy()
    action = {'index': {}}
    for key in ('_parent', '_percolate', '_routing', '_timestamp',
                '_ttl', '_type', '_version', '_version_type', '_id',
                '_retry_on_conflict'):
        if key in data:
            action['index'][key] = data.pop(key)

    return action, data.get('_source', data)


def bulk_index(client, docs, chunk_size=500, **kwargs):
    success, failed = 0, 0
    errors = []
    actions = map(expand_action, docs)

    while True:
        chunk = islice(actions, chunk_size)

        bulk_actions = []
        for action, data in chunk:
            bulk_actions.append(json.dumps(action))
            if data is not None:
                bulk_actions.append(json.dumps(data))

        if not bulk_actions:
            break

        body = "\n".join(bulk_actions) + "\n"
        response = client.bulk(body, **kwargs)

        if 'items' not in response:
            errors.append(response)
            return success, errors

        for op_type, item in map(methodcaller('popitem'), response['items']):
            ok = 200 <= item.get('status', 500) < 300
            if not ok:
                errors.append(item)
                failed += 1
            else:
                success += 1

            sublime.status_message("docs: {}".format(success + failed))

    return success, failed if not errors else errors


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
            chunk_size=500, scroll='5m', scan_kwargs={}, command=None):

    target_client = client if target_client is None else target_client

    result = {
        "_source": make_url(client.base_url, source_index),
        "_target": make_url(target_client.base_url, target_index),
    }

    docs = scan(client, query=query, index=source_index,
                scroll=scroll, **scan_kwargs)

    success, failed = bulk_index(
        target_client, change_index(docs, target_index),
        chunk_size=chunk_size, index=target_index)

    result['success'] = success
    result['failed'] = failed

    show_result_json(result, sort_keys=True, command=command)

copyindex = reindex


def dumpdata(outputfile, client, index, query=None,
             scroll='5m', scan_kwargs={}, command=None):

    result = {
        "_source": make_url(client.base_url, index),
        "_output": outputfile
    }

    docs = scan(client, query=query, index=index,
                scroll=scroll, **scan_kwargs)

    count = 0
    with gzip.open(outputfile, 'wb') as f:
        for doc in docs:
            del doc['_score']

            data = "{}\n".format(json.dumps(doc, ensure_ascii=False))
            f.write(bytes(data, 'utf-8'))

            count += 1
            sublime.status_message("dumps: {}".format(count))

    result['docs'] = count

    show_result_json(result, sort_keys=True, command=command)


def loaddata(inputfile, client, index, chunk_size=500, command=None):
    result = {
        "_target": make_url(client.base_url, index),
        "_input": inputfile
    }

    docs = []
    with gzip.open(inputfile, 'rb') as f:
        for doc in f:
            docs.append(json.loads(doc.decode('utf-8')))
            sublime.status_message("read: {}".format(len(docs)))

    success, failed = bulk_index(
        client, change_index(docs, index), chunk_size=chunk_size,
        index=index)

    result['success'] = success
    result['failed'] = failed

    show_result_json(result, sort_keys=True, command=command)


def analyze_keywords(client, index, body, analyzer='default', command=None):
    keywords = body.split('\n')
    items = []

    for keyword in keywords:
        if len(keyword) == 0:
            continue

        r = client.indices.analyze(
            index, keyword, params=dict(analyzer=analyzer))

        if 'tokens' not in r:
            show_result_json(r, command=command)
            return

        tokens = [t['token'] for t in r['tokens']]
        items.append(dict(keyword=keyword, analyzed=' / '.join(tokens)))

    show_result_json(items, command=command)
