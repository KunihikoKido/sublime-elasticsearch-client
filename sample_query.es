{
    "_source": {
        "include": [
            "title"
        ]
    },
    "aggs": {
        "genders": {
            "terms": {
                "field": "gender"
            }
        }
    },
    "query": {
        "filtered": {
            "filter": {
                "range": {
                    "created": {
                        "gte": "now - 1d / d"
                    }
                }
            },
            "query": {
                "match_all": {}
            }
        }
    }
}