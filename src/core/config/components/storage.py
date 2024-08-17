import abc
import logging
from typing import List, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError

from models.film import Film


class AbstractStorageHandler(abc.ABC):
    @abc.abstractmethod
    def get_by_id(self, model_id: str) -> Optional[Film]: ...

    @abc.abstractmethod
    def get_list(
        self, request: str, sort: dict = None, filters: dict = None, query: str = None
    ) -> Optional[List[Film]]: ...


class ElasticHandler(AbstractStorageHandler):
    def __init__(
        self,
        elastic: AsyncElasticsearch,
        model,
        model_index,
        search_query=None,
        filter_query=None,
    ):
        self.elastic = elastic
        self.model = model
        self.model_index = model_index
        self.search_query = search_query
        self.filter_query = filter_query

    async def get_by_id(self, model_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(index=self.model_index, id=model_id)
        except NotFoundError:
            return None
        return self.model(**doc["_source"])

    async def get_list(
        self, request: str, sort: dict = None, filters: dict = None, query: str = None
    ) -> Optional[List[Film]]:
        try:
            search_body = {
                "query": {"match_all": {}},
                "size": 10000,
            }

            if filters or query:
                search_body["query"] = {"bool": {"must": []}}

                if filters:
                    search_body["query"]["bool"]["must"].append(
                        {"match": {self.filter_query: filters.get("filter")}}
                    )

                if query:
                    search_body["query"]["bool"]["must"].append(
                        {"match": {self.search_query: query}}
                    )

            response = await self.elastic.search(
                index=self.model_index, body=search_body
            )

            data = [self.model(**doc["_source"]) for doc in response["hits"]["hits"]]

            return data

        except NotFoundError:
            logging.error("404 Not Found")
            return None
