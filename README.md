# Elasticsearch Client for Sublime Text 3

[![GitHub release](https://img.shields.io/github/release/KunihikoKido/sublime-elasticsearch-client.svg)](https://github.com/KunihikoKido/sublime-elasticsearch-client/releases)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/KunihikoKido/sublime-elasticsearch-client/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/KunihikoKido/sublime-elasticsearch-client.svg)](https://github.com/KunihikoKido/sublime-elasticsearch-client/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/KunihikoKido/sublime-elasticsearch-client.svg)](https://github.com/KunihikoKido/sublime-elasticsearch-client/issues)
[![GitHub forks](https://img.shields.io/github/forks/KunihikoKido/sublime-elasticsearch-client.svg)](https://github.com/KunihikoKido/sublime-elasticsearch-client/network)
[![Gratipay](https://img.shields.io/gratipay/KunihikoKido.svg)](https://gratipay.com/KunihikoKido/)
![Sublime Text](https://img.shields.io/badge/sublime_text-ST3-green.svg)
![Sublime Platforms](https://img.shields.io/badge/platforms-windows_osx_linux-green.svg)


Elasticsearch Client for Sublime Text

Elasticsearch Client allows you to build an Rest API request in Sublime Text and view the response in a panel.

## Overview

Elasticsearch Client integration: it's pretty handy.

![Command Palette](https://github.com/KunihikoKido/sublime-elasticsearch-client/wiki/images/palette.png)

## Options

- ``ab`` command: if use th ``Apache Bench`` command
- [PrettyJson](https://github.com/dzhibas/SublimePrettyJson) sublime plugin


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

Once you have a request ready, use shortcut ``Ctrl + Alt + S`` or open the Command Palette (``Shift + Command + P``) and enter ``Elasticsearch Request Body Search``.

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
            "doc_type": "test"
        },
        "api.siba.tokyo": {
            "base_url": "https://api.siba.tokyo/public/",
            "index": "index-zgkksx-my-index",
            "doc_type": "webpages"
        }
    },
    "ab_options": {
        "small":  ["-n", "10", "-c", "10"],
        "medium": ["-n", "100", "-c", "10"],
        "large":  ["-n", "1000", "-c", "10"],
    }
}
```

### Properties

Setting                    | Description
-------------------------- | ----------------------------------
``active_server``          | Elasticsearch Active Server. You can change the ``Switch Server`` Command
``servers``                | Elasticsearch Server settings.
``ab_command``             | Path to the Apache Bench (ab) command.
``ab_options``             | Apache Bench settings.
``enabled_pretty``         | enabled pretty json. required: [PrettyJson](https://github.com/dzhibas/SublimePrettyJson)
``pretty_command``         | pretty format command. default: ``pretty_json``
``pretty_syntax``          | pretty json target syntax. default: ``Elasticsearch``
``fixture_dir``            | Path to the Dump Data & Load Data command.


#### servers.\*

Setting                              | Description
------------------------------------ | ----------------------------------
``base_url``                         | Elasticsearch API Endpoint URL. default: ``http://localhost:9200``
``index``                            | Elasticsearch Index name. default: ``test``
``doc_type``                         | Elasticsearch Type name. default: ``test``
``analyzer``                         | analyzer for Analyze Command. default: ``default``
``http_headers``                     | Http header

**Note** Removed Access Control Options.

## Commands
open the Command Palette (``Shift + Command + P``) and enter ``Elasticsearch ...``.

### Command for Document APIs

* Elasticsearch: Bulk API
* Elasticsearch: Create Document
* Elasticsearch: Delete By Query
* Elasticsearch: Delete Document
* Elasticsearch: Delete Percolator
* Elasticsearch: Get Document
* Elasticsearch: Get Multiple Documents
* Elasticsearch: Get Source
* Elasticsearch: Index Document
* Elasticsearch: Index Percolator
* Elasticsearch: Multiple Termvector
* Elasticsearch: Termvector
* Elasticsearch: Update Document

### Command for Search APIs

* Elasticsearch: Clear Scroll
* Elasticsearch: Count
* Elasticsearch: Count Percolate
* Elasticsearch: Delete Search Template
* Elasticsearch: Explain Document
* Elasticsearch: Get Search Template
* Elasticsearch: More Like This
* Elasticsearch: Multiple Different Searches
* Elasticsearch: Multiple Percolate
* Elasticsearch: Percolate
* Elasticsearch: Put Search Template
* Elasticsearch: Request Body Search
* Elasticsearch: Request Body Search (search_type=count)
* Elasticsearch: Scan
* Elasticsearch: Scroll
* Elasticsearch: Search Exists
* Elasticsearch: Search Shards
* Elasticsearch: Search Template
* Elasticsearch: Search Template (search_type=count)
* Elasticsearch: Suggest
* Elasticsearch: URI Search
* Elasticsearch: Validate Query

### Command for Indices APIs

* Elasticsearch: Analyze Text
* Elasticsearch: Clear Index Cache
* Elasticsearch: Close Index
* Elasticsearch: Create Index
* Elasticsearch: Delete Index
* Elasticsearch: Delete Index Alias
* Elasticsearch: Delete Index Template
* Elasticsearch: Delete Index Warmer
* Elasticsearch: Delete Mapping
* Elasticsearch: Flush Index
* Elasticsearch: Get Field Mapping
* Elasticsearch: Get Index Alias
* Elasticsearch: Get Index Infomation
* Elasticsearch: Get Index Settings
* Elasticsearch: Get Index Template
* Elasticsearch: Get Index Warmer
* Elasticsearch: Get Mapping
* Elasticsearch: Get Upgrade Index Status
* Elasticsearch: Index Recovery Status
* Elasticsearch: Index Segments Infomation
* Elasticsearch: Index Stats
* Elasticsearch: Index Status
* Elasticsearch: Open Index
* Elasticsearch: Optimize Index
* Elasticsearch: Put Index Alias
* Elasticsearch: Put Index Settings
* Elasticsearch: Put Index Template
* Elasticsearch: Put Index Warmer
* Elasticsearch: Put Mapping
* Elasticsearch: Refresh Index
* Elasticsearch: Update Index Aliases
* Elasticsearch: Upgrade Index

### Command for Cluster APIs

* Elasticsearch: Cluster Health
* Elasticsearch: Cluster Info
* Elasticsearch: Cluster Pending Tasks
* Elasticsearch: Cluster Reroute
* Elasticsearch: Cluster State
* Elasticsearch: Cluster Stats
* Elasticsearch: Get Cluster Settngs
* Elasticsearch: Nodes hot_threads
* Elasticsearch: Nodes Info
* Elasticsearch: Nodes Shutdown
* Elasticsearch: Nodes Stats
* Elasticsearch: Put Cluster Settngs

### Command for Modules APIs

* Elasticsearch: Delete Script
* Elasticsearch: Get Script
* Elasticsearch: Put Script

### Command for Cat APIs

* Elasticsearch: Cat Aliases
* Elasticsearch: Cat Allocation
* Elasticsearch: Cat Count
* Elasticsearch: Cat Fielddata
* Elasticsearch: Cat Health
* Elasticsearch: Cat Help
* Elasticsearch: Cat Indices
* Elasticsearch: Cat Master
* Elasticsearch: Cat Nodes
* Elasticsearch: Cat Pending Tasks
* Elasticsearch: Cat Plugins
* Elasticsearch: Cat Recovery
* Elasticsearch: Cat Segments
* Elasticsearch: Cat Shards
* Elasticsearch: Cat Thread Pool

### Commmand for Query Benchmark

* Elasticsearch: Apache Bench
* Elasticsearch: Apache Bench for Search Template

### Commmand for Index Data Management.

* Elasticsearch: Reindex
* Elasticsearch: Dump Data
* Elasticsearch: Load Data
* Elasticsearch: Copy Data from ...

### Command for Sublime User Settings

* Elasticsearch: Switch Servers
* Elasticsearch: Show Active Server


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

## Screenshot

**Snippet**
![Snippet](https://github.com/KunihikoKido/sublime-elasticsearch-client/wiki/images/snippets.png)

**API Result**
![Show API Result](https://github.com/KunihikoKido/sublime-elasticsearch-client/wiki/images/show_result.png)

**Benchmarking**
![Benchmarking](https://github.com/KunihikoKido/sublime-elasticsearch-client/wiki/images/benchmarking.png)


---

Hello! Elasticsearch [日本語で](https://medium.com/hello-elasticsearch/elasticsearch-client-for-sublime-text-3-82b182d2417e)

