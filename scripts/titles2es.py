import argparse
import logging
import sys
import os
import csv

from search.config.mapping import DEFAULT_ES_MAPPING
from search.transformers.es_transformer import ESTransformer
from search.writers.es_writer import ESWriter

DEFAULT_ES_HOST = "localhost"
DEFAULT_ES_PORT = 9700
DEFAULT_ES_CHUNK_SIZE = 2
DEFAULT_INPUT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data/titles.csv"
)
logger = logging.getLogger()


def get_args():
    parser = argparse.ArgumentParser(
        description="Index titles from the MongoDB in Elasticsearch",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--es-host", help="Elasticsearch host", default=DEFAULT_ES_HOST)
    parser.add_argument(
        "--es-port", type=int, help="Elasticsearch port", default=DEFAULT_ES_PORT
    )
    parser.add_argument("--es-user", help="Elasticsearch user")
    parser.add_argument("--es-pass", help="Elasticsearch pass")
    parser.add_argument("--es-index", help="Elasticsearch index", required=True)
    parser.add_argument(
        "--es-mapping", help="Elasticsearch index mapping", default=DEFAULT_ES_MAPPING
    )
    parser.add_argument(
        "--es-chunk-size",
        help="maximum number of documents to index in a bulk request",
        type=int,
        default=DEFAULT_ES_CHUNK_SIZE,
    )
    parser.add_argument(
        "--input-file", help="Elasticsearch index", default=DEFAULT_INPUT_FILE
    )
    return parser.parse_args()


def configure_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger_es = logging.getLogger("elasticsearch")
    logger_es.setLevel(logging.WARNING)


def main():
    configure_logger()
    logger.info("Starting main")
    args = get_args()
    transformer = ESTransformer()
    writer = ESWriter(
        dict(
            host=args.es_host,
            port=args.es_port,
            index=args.es_index,
            mapping=args.es_mapping,
            user=args.es_user,
            password=args.es_pass,
        )
    )
    with open(args.input_file, "r") as in_file:
        writer.write_works(
            transformer.encode(row) for row in csv.DictReader(in_file, delimiter=",")
        )


if __name__ == "__main__":
    sys.exit(main())
