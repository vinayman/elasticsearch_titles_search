# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def install_reqs(filename):
    with open(filename) as fp:
        # filter comments and drop references to other requirements files
        reqs = [
            f for f in fp.readlines() if not f.startswith("-") and not f.startswith("#")
        ]
    return reqs


setup(
    name="elasticsarch_titles_search",
    version="0.1",
    # url="https://bitbucket.org/bmat-music/cisnet_avindex",
    license="Other/Proprietary License",
    author="vinaymanektalla@gmail.com",
    description="Use this to use an ElasticSearch Search Engine",
    packages=find_packages(exclude=["resources", "tests"]),
    include_package_data=True,
)
