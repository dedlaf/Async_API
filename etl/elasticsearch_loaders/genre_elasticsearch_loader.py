import backoff
from elasticsearch.helpers import bulk
from elasticsearch_loaders.elasticsearch_loader import ElasticsearchLoader
from schemas.genre import Genre


class GenreElasticsearchLoader(ElasticsearchLoader):

    @backoff.on_exception(backoff.expo, Exception, factor=2, max_time=600)
    def load(self, genres: list[Genre]) -> None:
        actions = [
            {"_index": "genres", "_id": genre.id, "_source": dict(genre)}
            for genre in genres
        ]

        bulk(self._es_client, actions, chunk_size=self._chunk_size)
