import logging
from datetime import datetime, timezone

from sql_queries import SQLQueries

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Fetcher:
    def __init__(self, __connection):
        self.__connection = __connection
        self.__cursor = self.__connection.cursor()
        self.queries = SQLQueries()

    def __fetch_query_all(self, query, s):
        self.__cursor.execute(query, (s,))
        return self.__cursor.fetchall()

    def __fetch_query(self, query, s):
        self.__cursor.execute(query, s)
        return self.__cursor.fetchone()

    def __delete_event(self, event_id):
        self.__cursor.execute(self.queries.DELETE_EVENT, (event_id,))
        self.__connection.commit()

    def _fetch_events(self):
        return self.__fetch_query_all(
            self.queries.GET_EVENT, (datetime.now(timezone.utc),)
        )

    def _fetch_template(self, template_id):
        return self.__fetch_query(self.queries.GET_TEMPLATE, (template_id,))[0]

    def _fetch_content(self, content_id):
        x = self.__fetch_query(SQLQueries.GET_CONTENT, (content_id,))[0]
        logging.info(x)
        return x

    def get_all(self):
        final_list = []
        for event_id, template_id, content_id, users, _ in self._fetch_events():
            final_dict = {
                "template": self._fetch_template(template_id),
                "content": self._fetch_content(content_id),
                "users": users[1:-1],
            }

            final_list.append(final_dict)
            self.__delete_event(event_id)
        return final_list
