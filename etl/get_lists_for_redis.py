import backoff
from config import backoff_configs, batch_size, final_data, redis_storage


@backoff.on_exception(**backoff_configs)
def merge_tuples(original_list: list) -> list:
    grouped_dict = {}
    for item in original_list:
        item_id = item[0]
        if item_id not in grouped_dict:
            grouped_dict[item_id] = []
        grouped_dict[item_id].append(item)

    merged_list = []
    for group_id, group_items in grouped_dict.items():
        movie_info = {
            "film_id": group_id,
            "title": group_items[0][1],
            "description": group_items[0][2],
            "rating": group_items[0][3],
            "fw_type": group_items[0][4],
            "created_at": group_items[0][5],
            "updated_at": group_items[0][6],
        }

        persons_set = set()
        for item in group_items:
            person_role = item[7]
            person_id = item[8]
            person_name = item[9]
            persons_set.add((person_role, person_id, person_name))
        persons = [
            {"id": role_id, "name": actor_name}
            for role, role_id, actor_name in persons_set
        ]

        genres_set = set([])
        for item in group_items:
            genre = item[10]
            genres_set.add(genre)
        genres = [genre for genre in genres_set]

        merged_list.append({**movie_info, "persons": persons, "genres": genres})
    return merged_list


@backoff.on_exception(**backoff_configs)
def get_list_of_persons(list_of_persons: list, cursor) -> None:
    while row := cursor.fetchmany(batch_size):
        all_persons = ", ".join([f"'{person[0]}'" for person in row])
        list_of_persons.append(all_persons)

    list_of_persons = ", ".join(list_of_persons)
    redis_storage.save_state(list_of_persons, "persons")


@backoff.on_exception(**backoff_configs)
def get_list_of_films_id(list_of_film: list, cursor) -> None:
    while True:
        row = cursor.fetchmany(batch_size)
        if not row:
            break
        fw = ", ".join([f"'{film[0]}'" for film in row])
        list_of_film.append(fw)
    list_of_film = ", ".join(list_of_film)
    redis_storage.save_state(list_of_film, "films_id")


@backoff.on_exception(**backoff_configs)
def get_list_of_films(final_data: list, cursor) -> None:
    while True:
        row = cursor.fetchmany(batch_size)
        if not row:
            break
        final_data.extend(merge_tuples(row))

    for item in final_data:
        redis_storage.save_state(item, item["film_id"])
