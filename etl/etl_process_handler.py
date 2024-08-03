from connection_manager import ConnectionManager
from data_handlers.filmwork_handler import FilmworkHandler
from data_handlers.genre_handler import GenreHandler
from state import State


class ETLProcessHandler:
    def __init__(self, state: State) -> None:
        self.__state = state

        self.__connection_manager = ConnectionManager()

        self.__filmwork_handler = FilmworkHandler(state, self.__connection_manager)
        self.__genre_handler = GenreHandler(state, self.__connection_manager)

    def handle_process(self) -> None:
        self.__handle_filmworks()
        self.__handle_genres()

    def __handle_filmworks(self) -> None:
        self.__filmwork_handler.handle_data()

    def __handle_genres(self) -> None:
        self.__genre_handler.handle_data()
