import itertools
import logging
from typing import Generator, List
import os
import certifi

from elasticsearch import Elasticsearch, helpers
from search.models import Title

logger = logging.getLogger(__name__)


class ESWriter:
    _BULK_THREAD_COUNT = 2

    def __init__(self, config: dict):
        self._config = config
        self.stats = dict(
            success=0,
            errors=0,
        )
        self._es = (
            Elasticsearch(
                [":".join([config["host"], str(config["port"])])],
                http_auth=(config["user"], config["password"]),
                use_ssl=True,
                ca_certs=certifi.where(),
                timeout=300,
            )
            if config["user"] and config["password"]
            else Elasticsearch(hosts=[dict(host=config["host"], port=config["port"])])
        )

    def write_works(
        self,
        works: Generator[Title, None, None],
        chunk_size: int = 5000,
    ):
        if not self._es.indices.exists(index=self._config["index"]):
            logger.info(f"Creating index {self._config['index']}")
            self._es.indices.create(
                index=self._config["index"], body=self._config["mapping"]
            )
        actions = self._titles_to_actions(self._config["index"], works)
        action_chunk = list(itertools.islice(actions, chunk_size))
        doc_indexed_count = 0
        while action_chunk:
            for success, info in helpers.parallel_bulk(
                self._es,
                action_chunk,
                thread_count=self._BULK_THREAD_COUNT,
                chunk_size=chunk_size,
                request_timeout=10000000,
            ):
                doc_indexed_count += 1
                if doc_indexed_count % chunk_size == 0:
                    logger.info(f"{doc_indexed_count:10} docs indexed")
            action_chunk = list(itertools.islice(actions, chunk_size))
        logger.info(f"{doc_indexed_count:10} docs indexed")
        self._es.indices.refresh()
        self.stats["success"] = doc_indexed_count
        self.stats["errors"] = 0

    def _titles_to_actions(
        self, index_name: str, titles: Generator[Title, None, None]
    ) -> List[dict]:
        for title in titles:
            yield dict(
                _op_type="index",
                _index=index_name,
                _source=title.to_native(),
            )
