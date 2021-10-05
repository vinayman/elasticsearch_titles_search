from typing import List, Tuple

from search.models import Title
from elasticsearch import Elasticsearch


class ESReader:
    def __init__(self, config):
        self._config = config
        self._es = Elasticsearch(hosts=[dict(host=config["host"], port=config["port"])])

    def find_all(self, skip_results: int = 1, max_results: int = 15):
        query_results = self._es.search(
            index=self._config["index"],
            body={},
            size=max_results,
            from_=(skip_results - 1) * max_results,
            track_total_hits=True,
        )
        works_total = query_results["hits"]["total"]
        works = []
        for query_result in query_results["hits"]["hits"]:
            works.append(Title(query_result["_source"]))
        return works, works_total

    def find_titles_by_title(
        self, query: dict, skip_results: int = 0, max_results: int = 50
    ) -> Tuple[List[Title], int]:
        query_results = self._es.search(
            index=self._config["index"],
            body=self._get_query_body_by_title(query, skip_results, max_results),
        )
        works_total = query_results["hits"]["total"]
        works = []
        for query_result in query_results["hits"]["hits"]:
            works.append(Title(query_result["_source"]))
        return works, works_total

    def find_by_title_id(
        self, title_id: str, skip_results: int = 0, max_results: int = 50
    ) -> Tuple[List[Title], int]:
        query_results = self._es.search(
            index=self._config["index"],
            body=self._get_query_body_by_title_id(title_id, skip_results, max_results),
        )
        works_total = query_results["hits"]["total"]
        works = []
        for query_result in query_results["hits"]["hits"]:
            works.append(Title(query_result["_source"]))
        return works, works_total

    def _get_query_body_by_title_id(self, title_id: str, _from: int, size: int):
        body_query = dict(
            bool=dict(
                must=[
                    dict(match=dict(title_id=title_id)),
                ]
            )
        )
        body = {
            "from": _from,
            "size": size,
            "query": body_query,
        }
        return body

    def _get_query_body_by_title(self, query: dict, _from: int, size: int) -> dict:
        body_query = dict(
            bool=dict(
                must=[
                    dict(match=dict(titles=query["title"])),
                ]
            )
        )
        body = {
            "from": _from,
            "size": size,
            "query": body_query,
        }
        return body

    def find_titles_by_prefix(
        self, prefix: str, max_results: int = 20, fuzziness: int = 0
    ) -> List[Title]:
        query_body = dict(
            suggest=dict(
                titles=dict(
                    prefix=prefix,
                    completion=dict(
                        size=max_results,
                        field="titles_prefixes",
                        fuzzy=dict(
                            fuzziness=fuzziness,
                        ),
                    ),
                )
            )
        )
        query_results = self._es.search(index=self._config["index"], body=query_body)
        for query_result in query_results["suggest"]["titles"][0]["options"]:
            yield Title(query_result["_source"])
