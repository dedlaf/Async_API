import abc
import json
from typing import Any

from enums import StorageKey


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> dict[str, Any]:
        """Получить состояние из хранилища."""


class JsonFileStorage(BaseStorage):
    """Реализация хранилища, использующего локальный файл.

    Формат хранения: JSON
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        with open(self.file_path, "w") as file:
            json.dump(state, file)

    def retrieve_state(self) -> dict[str, Any]:
        """Получить состояние из хранилища."""
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}


class State:
    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage
        self.state = self.storage.retrieve_state()

    def set_last_modified(self, last_modified: str) -> None:
        self.state[StorageKey.LAST_MODIFIED_FILMWORK.value] = last_modified
        self.state[StorageKey.LAST_MODIFIED_GENRE.value] = last_modified
        self.storage.save_state(self.state)

    def set_last_modified_filmwork(self, last_modified: str) -> None:
        self.state[StorageKey.LAST_MODIFIED_FILMWORK.value] = last_modified
        self.storage.save_state(self.state)

    def set_last_modified_genre(self, last_modified: str) -> None:
        self.state[StorageKey.LAST_MODIFIED_GENRE.value] = last_modified
        self.storage.save_state(self.state)

    def get_last_modified_filmwork(self) -> str:
        return self.state.get(StorageKey.LAST_MODIFIED_FILMWORK.value)

    def get_last_modified_genre(self) -> str:
        return self.state.get(StorageKey.LAST_MODIFIED_GENRE.value)
