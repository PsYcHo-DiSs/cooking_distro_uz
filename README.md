# 🥘 Cooking Distro UZ — Django веб-приложение

Платформа для публикации, просмотра и комментирования кулинарных рецептов с кэшированием, админкой и системой категорий.

---

## ✅ Функциональность

- 📄 Публикация и просмотр статей
- 🏷️ Сортировка по категориям
- 👥 Авторизация / регистрация
- 💬 Комментарии к постам
- 🔝 Блок рекомендательных постов (по просмотрам)
- ⚡ Кэширование с поддержкой Redis или файловой системы
- 🛠️ Docker-сборка всего стека (PostgreSQL + Redis + Django)

---

## 🧠 Технологический стек

| Компонент      | Используется                        |
|----------------|-------------------------------------|
| Backend        | Python 3.12 + Django                |
| БД             | PostgreSQL 15                       |
| Кэш            | Redis или FileBasedCache            |
| Докеризация    | Docker + Docker Compose             |
| Интерфейс      | HTML + Bootstrap                    |
| Прочее         | Django REST Framework, Swagger (drf-yasg) |

---

## 📦 Структура проекта

```
.
├── docker-compose.yml             # Контейнеры: Django, Redis, PostgreSQL
├── Dockerfile                     # Сборка Django-приложения
├── entrypoint.sh                  # Скрипт запуска (миграции, суперюзер, сервер)
├── requirements.txt               # Зависимости проекта
├── manage.py                      # Django CLI
├── .env                           # Настройки окружения
├── .env.example                   # Шаблон .env файла
├── conf/                          # Основные конфиги Django
│   └── settings.py                # Конфигурация проекта
├── cooking/                       # Django-приложение
│   ├── models.py                  # Модели Post, Category, Comment
│   ├── views.py                   # Отображения
│   ├── forms.py                   # Django-формы
│   ├── templatetags/blog_tags.py # Теги + кэш логика
│   ├── urls.py                    # URL-маршруты
├── templates/                     # HTML-шаблоны
└── media/                         # Загружаемые изображения
```

---

## ⚙️ Переменные окружения

Создай `.env` на основе `.env.example`:

```ini
SECRET_KEY='...'

USE_REDIS_CACHE=True
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=1

DB_USER=postgres
DB_NAME=cooking_django_db
DB_PASSWORD=321
DB_ADDRESS=db
DB_PORT=5432
```

---

## 🚀 Запуск проекта (Docker)

```bash
git clone https://github.com/PsYcHo-DiSs/cooking_distro_uz.git
cd cooking_distro_uz
cp .env.example .env
docker-compose up --build
```

Открой в браузере: [http://localhost:8000](http://localhost:8000)

После запуска:
- Админка: `admin:1`
- Swagger: `/swagger/` (если подключено в `urls.py`)

---

## 🧪 Для разработки без Docker

> ⚠️ Предполагается, что Redis и PostgreSQL уже запущены отдельно (например, через Docker Desktop).

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

---

## 🧰 Компоненты и их роль

| Компонент     | Назначение |
|---------------|------------|
| `entrypoint.sh` | Ожидание БД, миграции, создание суперпользователя |
| `templatetags/blog_tags.py` | Кэширование популярных постов и категорий |
| `USE_REDIS_CACHE` | Включение Redis или файлового кеша через `.env` |

---

## 📸 Примеры кэширования

**Популярные посты** (в шаблоне):

```django
{% load blog_tags %}
{% get_top_5_posts as recommended_posts %}
{% for post in recommended_posts %}
    ...
{% endfor %}
```

**В `blog_tags.py`**:

```python
@register.simple_tag()
def get_top_5_posts():
    top = cache.get('top_5_posts')
    if not top:
        top = Post.objects.filter(is_published=True).order_by('-watched')[:5]
        cache.set('top_5_posts', top, 60)
    return top
```

---

## 📌 Примечания

- ⚠️ Кэш может не отражать актуальные изменения сразу
- Проект можно масштабировать и подключить Celery для задач (отложено)