DEFAULT_ES_MAPPING = {
    "mappings": {
        "properties": {
            "titles_prefixes": {
                "type": "completion",
            },
            "_titles": {"type": "text", "norms": False, "index_options": "docs"},
        }
    }
}
