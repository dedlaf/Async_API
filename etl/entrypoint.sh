#!/bin/sh

check_db() {
  PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'
}

echo "Ожидание подключения к бд"
while ! check_db; do
  sleep 1
done
echo "Удалось подключиться к бд"

echo "Ожидание подключения к es"
while ! curl -sS $ELASTIC_HOST; do
  sleep 1;
done
echo "Удалось подключиться к es"

echo "Создание индекса жанров"
curl -XPUT "$ELASTIC_HOST" -H 'Content-Type: application/json' -d @"$GENRES_MAPPING_FILE"

echo "Создание индекса фильмов"
curl -XPUT "$ELASTIC_HOST" -H 'Content-Type: application/json' -d @"$MOVIES_MAPPING_FILE"

echo "Создание индекса персон"
curl -XPUT "$ELASTIC_HOST" -H 'Content-Type: application/json' -d @"$PERSONS_MAPPING_FILE"

echo "Запуск сервера"
python etl_process.py --date="$DATE"
