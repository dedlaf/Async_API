#!/bin/sh

check_db() {
  PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'
}
check_es() {
  curl -s "$ELASTIC_HOST" > /dev/null
  return $?
}

echo "Ожидание подключения к бд"
while ! check_db; do
  sleep 1
done
echo "Удалось подключиться к бд"

echo "Ожидание подключения к es"
until check_es; do
  sleep 1
done
echo "Удалось подключиться к es"

MAPPING_FILE="index_mapping.json"

echo "Создание индекса"
curl -XPUT "$ELASTIC_HOST" -H 'Content-Type: application/json' -d @"$MAPPING_FILE"

echo "Запуск сервера"
python etl_process.py --date="$DATE"

