from abc import abstractmethod
from typing import Any

import backoff


class ElasticsearchLoader:
    def __init__(self, chunk_size: int, es_client: Any) -> None:
        self._es_client = es_client
        self._chunk_size = chunk_size

    @abstractmethod
    @backoff.on_exception(backoff.expo, Exception, factor=2, max_time=600)
    def load(self, data: list[Any]) -> None: ...
