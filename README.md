# Elasticsearch Client for Sublime Text 3
Elasticsearch Client for Sublime Text

Elasticsearch Client allows you to build an Rest API request in Sublime Text and view the response in a panel.

## Overview

Elasticsearch Client integration: it's pretty handy.

![Command Palette](https://github.com/KunihikoKido/sublime-elasticsearch-client/wiki/images/palette.png)

## Required

- ``curl`` command (required) you need have cURL installed
- ``ab`` command (optional) if use th ``Apache Bench`` command
- [PrettyJson](https://github.com/dzhibas/SublimePrettyJson) sublime plugin (optional) 

## Installation

### Package Control
The easiest way to install this is with [Package Control](https://packagecontrol.io/packages/ElasticsearchClient).

1. To open the command palette, press ``ctrl+shift+p`` (Win, Linux) or ``cmd+shift+p`` (OS X). 
2. Enter ``Package Control: Install Package``
3. Search for ``ElasticsearchClient`` and hit Enter to install.

### Manual
To install, clone to your "Packages" directory.

1. Click the ``Preferences > Browse Packages`` menu
2. Open up a terminal and execute the following:

```shell
git clone https://github.com/kunihikokido/sublime-elasticsearch-client.git ElasticsearchClient
```

**Note** Elasticsearch Client expects to be installed to a directory called "ElasticsearchClient". Some features like the meny command to open settings will not work if installed somewhere else.

## Using
you can send a body

```json
{
    "query": {
        "match_all": {}
    }
}
```

Once you have a request ready, use shortcut ``Ctrl + Alt + S`` or open the Command Palette (``Shift + Command + P``) and enter ``Elasticsearch Search``.

## Settings

User Settings (accessible from the *Preferences/Package Settings/Elasticsearch Client/Settings - User* menu)

*Example:*

```js
{
    "active_server": "localhost",
    "servers": {
        "localhost": {
            "base_url": "http://localhost:9200/",
            "index": "test",
            "doc_type": "test",
            "analyzer": "default",
            "enabled_create_index": true,
            "enabled_delete_mapping": true,
            "enabled_delete_document": true,
            "enabled_delete_index": true,
            "enabled_index_document": true,
            "enabled_put_mapping": true,
            "enabled_register_query": true,
            "enabled_delete_percolator": true,
        },
        "api.siba.tokyo": {
            "base_url": "https://api.siba.tokyo/public/",
            "index": "index-zgkksx-my-index",
            "doc_type": "webpages"
        }
    },
    "benchmarks": {
        "default": {
            "requests": 100,
            "concurrency": 10,
        }
    }
}
```

### Properties

Setting                    | Description
-------------------------- | ----------------------------------
``active_server``          | Elasticsearch Active Server. You can change the ``Switch Server`` Command
``servers``                | Elasticsearch Server settings.
``benchmarks``             | Apache Bench settings.
``quiet``                  | if set ``false`` information running about prints the request command. (View/Show Console menu)
``curl_command``           | Path to the curl command.
``ab_command``             | Path to the Apache Bench (ab) command.
``enabled_pretty``         | enabled pretty json. required: [PrettyJson](https://github.com/dzhibas/SublimePrettyJson)
``pretty_command``         | pretty format command. default: ``pretty_json``
``pretty_syntax``          | pretty json target syntax. default: ``Elasticsearch``
``ask_to_search_types``    | if ``true`` you can choice search_types.


#### servers.\*

Setting                       | Description
----------------------------- | ----------------------------------
``base_url``                  | Elasticsearch API Endpoint URL. default: ``http://localhost:9200``
``index``                     | Elasticsearch Index name. default: ``test``
``doc_type``                  | Elasticsearch Type name. default: ``test``
``analyzer``                  | analyzer for Analyze Command. default: ``default``
``enabled_create_index``      | if set ``true`` you can create index. default: ``false``
``enabled_delete_mapping``    | if set ``true`` you can delete mapping. default: ``false``
``enabled_delete_document``   | if set ``true`` you can delete document. default: ``false``
``enabled_delete_index``      | if set ``true`` you can delete index. default: ``false``
``enabled_index_document``    | if set ``true`` you can index document. default: ``false``
``enabled_put_mapping``       | if set ``true`` you can put mapping. default: ``false``
``enabled_register_query``    | if set ``true`` you can register query for percolator. default: ``false``
``enabled_delete_percolator`` | if set ``true`` you can delete registerd query for percolator. default: ``false``
``enabled_put_warmer``        | if set ``true`` you can register warmer. default: ``false``
``enabled_delete_warmer``     | if set ``true`` you can delete warmer. default: ``false``
``enabled_add_alias``         | if set ``true`` you can add alias. default: ``false``
``enabled_delete_alias``      | if set ``true`` you can delete alias. default: ``false``

#### benchmarks.\*

Setting                    | Description
-------------------------- | ----------------------------------
``requests``               | Number of requests to perform
``concurrency``            | Number of multiple requests to make at a time



## Commands
open the Command Palette (``Shift + Command + P``) and enter ``Elasticsearch ...``.

### Command for Search APIs

Command                                           | Method    | Call API
------------------------------------------------- | --------- | -------------------------
Elasticsearch: Analyze                            | POST      | ``/index/_analyze``
Elasticsearch: Benchmark                          | PUT       | ``/_bench``
Elasticsearch: Explain Document                   | POST      | ``/index/type/id/_explain``
Elasticsearch: Register Query (Percolator)        | PUT       | ``/index/.percolator/id``
Elasticsearch: Search Request                     | POST      | ``/index/type/_search``
Elasticsearch: Show Registered Query (Percolator) | POST      | ``/index/type/_percolate``
Elasticsearch: UN-Register Query (Percolator)     | DELETE    | ``/index/.percolator/id``


### Command for Document APIs

Command                            | Method    | Call API
---------------------------------- | --------- | -------------------------
Elasticsearch: Delete Document     | DELETE    | ``/index/type/id``
Elasticsearch: Index Document      | PUT/POST  | ``/index/type/id``
Elasticsearch: Get Document        | GET       | ``/index/type/id``

### Command for Index APIs

Command                              | Method    | Call API
------------------------------------ | --------- | -------------------------
Elasticsearch: Create Index          | PUT       | ``/index``
Elasticsearch: Delete Index          | DELETE    | ``/index/``
Elasticsearch: Get Index Settings    | GET       | ``/index/_settings``
Elasticsearch: Delete Mapping        | DELETE    | ``/index/_mapping/type``
Elasticsearch: Get Mapping           | GET       | ``/index/_mapping/type``
Elasticsearch: Put Mapping           | PUT       | ``/index/_mapping/type``
Elasticsearch: Get Warmer            | GET       | ``/index/_warmer/name``
Elasticsearch: Delete Warmer         | DELETE    | ``/index/_warmer/name``
Elasticsearch: Put Warmer            | PUT       | ``/index/_warmer/name``
Elasticsearch: Add Alias             | PUT       | ``/index/_alias/name``
Elasticsearch: Add Alias with Filter | PUT       | ``/index/_alias/name``
Elasticsearch: Delete Alias          | DELETE    | ``/index/_alias/name``
Elasticsearch: Get Alias             | GET       | ``/index/_alias/name``


### Command for Cat APIs

Command                            | Method    | Call API
---------------------------------- | --------- | -------------------------
Elasticsearch: Cat Health          | GET       | ``/_cat/health``
Elasticsearch: Cat Shards          | GET       | ``/_cat/shards/index``
Elasticsearch: Cat Indexes         | GET       | ``/_cat/indices/index``
Elasticsearch: Cat Aliases         | GET       | ``/_cat/aliases/alias``
Elasticsearch: Cat Allocation      | GET       | ``/_cat/allocation``
Elasticsearch: Cat Master          | GET       | ``/_cat/master``
Elasticsearch: Cat Nodes           | GET       | ``/_cat/nodes``
Elasticsearch: Cat Pending Tasks   | GET       | ``/_cat/pending_tasks``
Elasticsearch: Cat Plugins         | GET       | ``/_cat/plugins``
Elasticsearch: Cat Recovery        | GET       | ``/_cat/recovery``
Elasticsearch: Cat Thread Pool     | GET       | ``/_cat/thread_pool``
Elasticsearch: Cat Segments        | GET       | ``/_cat/segments``


### Utility Commands

Command                                | Descrption
-------------------------------------- | -------------------------
Elasticsearch: Apach Bench             | Run Benchmark.
Elasticsearch: Open Reference          | Open Elasticsearch Reference Webpage
Elasticsearch: Show Active Server      | Show active server settings in a panel.
Elasticsearch: Switch Servers          | Change the active server.
Elasticsearch: User File Settings      | Shortcut. ``Preferences > Package Settings > ElasticsearchClient > Settings – User`` menu
Elasticsearch: Search in Docs          | Site Search


## Snippets for Queries
file types ``*.es`` or set syntax ``Elasticsearch``

Abbreviation                    | tag
------------------------------- | ----------------------------------
bool                            | ``"bool": {...}``
boosting                        | ``"boosting": {...}``
commonterms                     | ``"common": {...}``
constantscore                   | ``"constant_score": {...}``
dismax                          | ``"dis_max": {...}``
filtered                        | ``"filtered": {...}``
functionscore                   | ``"function_score": {...}``
fuzzy                           | ``"fuzzy": {...}``
fuzzylike                       | ``"fuzzy_like_this": {...}``
fuzzylike                       | ``"fuzzy_like_this_field": {...}``
geoshape                        | ``"geo_shape": {...}``
haschild                        | ``"has_child": {...}``
ids                             | ``"ids": {...}``
indices                         | ``"indices": {...}``
matchall                        | ``"match_all": {..}``
match                           | ``"match": {...}``
morelike                        | ``"more_like_this": {...}``
multimatch                      | ``"multi_match": {...}``
nested                          | ``"nested": {...}``
prefix                          | ``"prefix": {...}``
querystring                     | ``"query_string": {...}``
range                           | ``"range": {...}``
regexp                          | ``"regexp": {...}``
simplequery                     | ``"simple_query_string": {...}``
spanfirst                       | ``"span_first": {...}``
spannear                        | ``"span_near": {...}``
spanmulti                       | ``"span_multi": {...}``
spannot                         | ``"span_not": {..}``
spanor                          | ``"span_or": {...}``
template                        | ``"template": {...}``
term                            | ``"term": {...}``
terms                           | ``"terms": {...}``
topchildren                     | ``"top_children": {...}``
wildcard                        | ``"wildcard": {...}``

## Snippets for Filters
file types ``*.es`` or set syntax ``Elasticsearch``

Abbreviation                    | tag
------------------------------- | ----------------------------------
and                             | ``"and": [...]``
bool                            | ``"bool": {...}``
exists                          | ``"exists": {...}``
geobox                          | ``"geo_bounding_box": {...}``
geodistance                     | ``"geo_distance": {...}``
geopolygon                      | ``"geo_polygon": {...}``
geoshape                        | ``"geo_shape": {...}``
geohash                         | ``"geohash_cell": {...}``
haschild                        | ``"has_child": {...}``
hascparent                      | ``"has_parent": {...}``
ids                             | ``"ids": {...}``
indices                         | ``"indices": {...}``
limit                           | ``"limit": {...}``
matchall                        | ``"match_all": {..}``
missing                         | ``"missing": {...}``
nested                          | ``"nested": {...}``
not                             | ``"not": [...]``
or                              | ``"or": [...]``
prefix                          | ``"prefix": {...}``
range                           | ``"range": {...}``
regexp                          | ``"regexp": {...}``
script                          | ``"script": {...}``
term                            | ``"term": {...}``
terms                           | ``"terms": {...}``
type                            | ``"type": {...}``

## Snippets for Aggregations
file types ``*.es`` or set syntax ``Elasticsearch``

Abbreviation                    | tag
------------------------------- | ----------------------------------
avg                             | ``"aggs": {..."avg": {...}``
cardinality                     | ``"aggs": {..."cardinality": {...}``
children                        | ``"aggs": {..."children": {...}``
datehistogram                   | ``"aggs": {..."date_histogram": {...}``
daterange                       | ``"aggs": {..."date_range": {...}``
extendedstats                   | ``"aggs": {..."extended_stats": {...}``
filter                          | ``"aggs": {..."filter": {...}``
filters                         | ``"aggs": {..."filters": {...}``
geobounds                       | ``"aggs": {..."geo_bounds": {...}``
geodistance                     | ``"aggs": {..."geo_distance": {...}``
geohash                         | ``"aggs": {..."geohash_grid": {...}``
global                          | ``"aggs": {..."global": {...}``
histogram                       | ``"aggs": {..."histogram": {...}``
ipv4range                       | ``"aggs": {..."ip_range": {...}``
max                             | ``"aggs": {..."max": {...}``
min                             | ``"aggs": {..."min": {...}``
missing                         | ``"aggs": {..."missing": {...}``
nested                          | ``"aggs": {..."nested": {...}``
percentileranks                 | ``"aggs": {..."percentile_ranks": {...}``
percentiles                     | ``"aggs": {..."percentiles": {...}``
range                           | ``"aggs": {..."range": {...}``
reversenested                   | ``"aggs": {..."reverse_nested": {...}``
scriptedmetric                  | ``"aggs": {..."scripted_metric": {...}``
significantterm                 | ``"aggs": {..."significant_terms": {...}``
stats                           | ``"aggs": {..."stats": {...}``
sum                             | ``"aggs": {..."sum": {...}``
terms                           | ``"aggs": {..."terms": {...}``
tophits                         | ``"aggs": {..."top_hits": {...}``
valuecount                      | ``"aggs": {..."value_count": {...}``


## Completions
file types ``*.es`` or set syntax ``Elasticsearch``

- _all
- _score
- asc
- desc
- false
- true

and etc..

---

Hello! Elasticsearch [日本語で](https://medium.com/hello-elasticsearch/elasticsearch-client-for-sublime-text-3-82b182d2417e)

