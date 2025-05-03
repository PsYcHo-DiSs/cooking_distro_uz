#!/bin/sh

echo "Ожидаем доступности PostgreSQL..."
until pg_isready -h "$DB_ADDRESS" -p "$DB_PORT" -U "$DB_USER"; do
  >&2 echo "Postgres недоступен - ждём..."
  sleep 1
done

echo "🚀 Применяем миграции..."
python manage.py migrate

echo "🔐 Создаём суперпользователя..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', '1')
EOF

echo "✅ Запускаем Django-сервер..."
exec python manage.py runserver 0.0.0.0:8000