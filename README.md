# Elasticsearch Client for ST3

Elasticsearch Client allows you to build an Rest API request in Sublime Text 3 and view the response in a panel.

![orverview](https://raw.githubusercontent.com/KunihikoKido/sublime-elasticsearch-client/master/screenshots/search.gif)

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

Once you have a request ready, use shortcut ``Ctrl + Alt + S`` or open the Command Palette (``Shift + Command + P``) and enter ``elasticsearch search request body``.

## Settings

User Settings (accessible from the *Preferences/Package Settings/Elasticsearch Client/Settings - User* menu)

*Example:*

```js
{
  "base_url": "http://localhost:9200",
  "index": "blog",
  "doc_type": "posts",
  "servers": [
      {
          "base_url": "http://localhost:9200",
          "index": "blog",
          "doc_type": "posts",
      },
      {
          "base_url": "http://localhost:9200",
          "index": "twitter",
          "doc_type": "tweets",
      }
  ]
}
```

You can switch the server, use ``Elasticsearch: Settings Switch Server`` command.

## Snippets
Currently this should work in ``.json`` or ``.es``

## Commands

### Command for Search & Document APIs

* Elasticsearch: Bulk
* Elasticsearch: Clear Scroll
* Elasticsearch: Count
* Elasticsearch: Count Percolate
* Elasticsearch: Create Document
* Elasticsearch: Delete By Query
* Elasticsearch: Delete Document
* Elasticsearch: Delete Script
* Elasticsearch: Delete Search Template
* Elasticsearch: Exists Document
* Elasticsearch: Explain Document
* Elasticsearch: Field Stats
* Elasticsearch: Get Document
* Elasticsearch: Get Document Source
* Elasticsearch: Get Multiple Documents
* Elasticsearch: Get Percolator Query
* Elasticsearch: Get Script
* Elasticsearch: Get Search Template
* Elasticsearch: Index Document
* Elasticsearch: Index Percolator Query
* Elasticsearch: Info
* Elasticsearch: Multiple Percolate
* Elasticsearch: Multiple Search
* Elasticsearch: Multiple Termvectors
* Elasticsearch: Percolate
* Elasticsearch: Ping
* Elasticsearch: Put Script
* Elasticsearch: Put Search Template
* Elasticsearch: Scroll
* Elasticsearch: Search Exists
* Elasticsearch: Search Percolator Query
* Elasticsearch: Search Request Body
* Elasticsearch: Search Request Body Count
* Elasticsearch: Search Request Body Scan
* Elasticsearch: Search Shards
* Elasticsearch: Search Simple Query
* Elasticsearch: Search Template
* Elasticsearch: Search Template Count
* Elasticsearch: Search Template Scan
* Elasticsearch: Suggest
* Elasticsearch: Termvector
* Elasticsearch: Update Document


### Command for Cat APIs

* Elasticsearch: Cat Aliases
* Elasticsearch: Cat Allocation
* Elasticsearch: Cat Count
* Elasticsearch: Cat Fielddata
* Elasticsearch: Cat Health
* Elasticsearch: Cat Indices
* Elasticsearch: Cat Master
* Elasticsearch: Cat Nodes
* Elasticsearch: Cat Pending Tasks
* Elasticsearch: Cat Plugins
* Elasticsearch: Cat Recovery
* Elasticsearch: Cat Segments
* Elasticsearch: Cat Shards
* Elasticsearch: Cat Thread Pool

### Command for Cluster APIs

* Elasticsearch: Cluster Get Settings
* Elasticsearch: Cluster Health
* Elasticsearch: Cluster Pending Tasks
* Elasticsearch: Cluster Put Settings
* Elasticsearch: Cluster Reroute
* Elasticsearch: Cluster State
* Elasticsearch: Cluster Stats

### Command for Indices APIs

* Elasticsearch: Indices Analyze
* Elasticsearch: Indices Clear Cache
* Elasticsearch: Indices Close
* Elasticsearch: Indices Create
* Elasticsearch: Indices Create Doc Type
* Elasticsearch: Indices Delete
* Elasticsearch: Indices Delete Alias
* Elasticsearch: Indices Delete Mapping
* Elasticsearch: Indices Delete Template
* Elasticsearch: Indices Delete Warmer
* Elasticsearch: Indices Exists
* Elasticsearch: Indices Exists Alias
* Elasticsearch: Indices Exists Doc Type
* Elasticsearch: Indices Exists Template
* Elasticsearch: Indices Flush
* Elasticsearch: Indices Flush Synced
* Elasticsearch: Indices Get
* Elasticsearch: Indices Get Alias
* Elasticsearch: Indices Get Field Mapping
* Elasticsearch: Indices Get Mapping
* Elasticsearch: Indices Get Settings
* Elasticsearch: Indices Get Template
* Elasticsearch: Indices Get Upgrade
* Elasticsearch: Indices Get Warmer
* Elasticsearch: Indices Open
* Elasticsearch: Indices Optimize
* Elasticsearch: Indices Put Alias
* Elasticsearch: Indices Put Mapping
* Elasticsearch: Indices Put Settings
* Elasticsearch: Indices Put Template
* Elasticsearch: Indices Put Warmer
* Elasticsearch: Indices Recovery
* Elasticsearch: Indices Refresh
* Elasticsearch: Indices Segments
* Elasticsearch: Indices Stats
* Elasticsearch: Indices Status
* Elasticsearch: Indices Update Aliases
* Elasticsearch: Indices Upgrade
* Elasticsearch: Indices Validate Query

### Command for Nodes APIs

* Elasticsearch: Nodes Hot Threads
* Elasticsearch: Nodes Info
* Elasticsearch: Nodes Shutdown All
* Elasticsearch: Nodes Shutdown Local
* Elasticsearch: Nodes Shutdown Master

### Command for Snapshot APIs

* Elasticsearch: Snapshot Create
* Elasticsearch: Snapshot Create Repository
* Elasticsearch: Snapshot Delete
* Elasticsearch: Snapshot Delete Repository
* Elasticsearch: Snapshot Get
* Elasticsearch: Snapshot Get Repository
* Elasticsearch: Snapshot Restore
* Elasticsearch: Snapshot Status
* Elasticsearch: Snapshot Verify Repository

### Helper Commands

* Elasticsearch: Helper Benchmark For Search Request Body
* Elasticsearch: Helper Benchmark For Search Request Body Count
* Elasticsearch: Helper Benchmark For Search Template
* Elasticsearch: Helper Benchmark For Search Template Count
* Elasticsearch: Helper Change Number Of Replicas
* Elasticsearch: Helper Close Open Index
* Elasticsearch: Helper Convert Csv Bulk Index
* Elasticsearch: Helper Dump Index Data
* Elasticsearch: Helper Import Csv
* Elasticsearch: Helper Load Index Data
* Elasticsearch: Helper Reindex


### Command for User Settings

* Elasticsearch: Settings Select Doc Type
* Elasticsearch: Settings Select Index
* Elasticsearch: Settings Show Active Server
* Elasticsearch: Settings Switch Server


## Screenshots

### Search Request Body Command
![search](https://raw.githubusercontent.com/KunihikoKido/sublime-elasticsearch-client/master/screenshots/search.gif)

### Cat Api Command
![cat](https://raw.githubusercontent.com/KunihikoKido/sublime-elasticsearch-client/master/screenshots/cat.gif)

## Helper Reindex Command
![reindex](https://raw.githubusercontent.com/KunihikoKido/sublime-elasticsearch-client/master/screenshots/reindex.gif)

## Helper Benchmark
![reindex](https://raw.githubusercontent.com/KunihikoKido/sublime-elasticsearch-client/master/screenshots/benchmark.gif)
