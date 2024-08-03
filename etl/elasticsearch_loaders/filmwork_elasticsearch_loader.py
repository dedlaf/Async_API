import backoff
from elasticsearch.helpers import bulk
from elasticsearch_loaders.elasticsearch_loader import ElasticsearchLoader
from schemas.filmwork import Filmwork


class FilmworkElasticsearchLoader(ElasticsearchLoader):

    @backoff.on_exception(backoff.expo, Exception, factor=2, max_time=600)
    def load(self, filmworks: list[Filmwork]) -> None:
        actions = [
            {"_index": "movies", "_id": filmwork.id, "_source": dict(filmwork)}
            for filmwork in filmworks
        ]

        bulk(self._es_client, actions, chunk_size=self._chunk_size)
