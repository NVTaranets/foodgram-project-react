# Продуктовый помощник

Досупен по [ссылке](http://foodgram-nvt.tk)

<details>
  <summary> Админка </summary>

```py
email: rev@rev.ru
password: asdfQWER12#$
```

</details>

## Оглавление

- [Технологии](#технологии)
- [Описание](#описание)
- <a href="#structure"> Установка </a>
- [Автор](#автор)

## Технологии

- Python;
- Django-Rest-Framework;
- Gunicorn;
- Docker/Docker-compose;
- Nginx;
- PostgreSQL;
- pgAdmin
- Portainer
- Yandex.Cloud.

[⬆️Оглавление](#оглавление)

## Описание

 Онлайн-сервис, где пользователи могут:

- публиковать рецепты;
- подписываться на публикации других пользователей;
- добавлять понравившиеся рецепты в список «Избранное»;
- перед походом в магазин скачивать сводный список продуктов.

[⬆️Оглавление](#оглавление)

<details>
  <summary>
    <h2 id="structure"> Установка </h2>
  </summary>

### Структура проекта:

```cmd
|   .gitignore
|   README.md
|   setup.cfg
|
+---.github  <-- Action для CI/CD проекта
|   \---workflows
|           ci-cd.yml
|
+---backend
|   \---foodgram  <-- Бекенд проекта "Продуктовый помошник"
|       |   db.sqlite3
|       |   Dockerfile
|       |   manage.py
|       |   requirements.txt
|       |
|       +---api
|       |       apps.py
|       |       filters.py
|       |       pagination.py
|       |       permissions.py
|       |       serializers.py
|       |       urls.py
|       |       utilites.py
|       |       views.py
|       |       __init__.py
|       |
|       +---fonts
|       |       times.ttf
|       |
|       +---foodgram
|       |       asgi.py
|       |       settings.py
|       |       urls.py
|       |       wsgi.py
|       |       __init__.py
|       |
|       +---media
|       |   \---recipes
|       |
|       +---recipes
|       |   |   admin.py
|       |   |   apps.py
|       |   |   models.py
|       |   |   __init__.py
|       |   |
|       |   +---management
|       |       |   __init__.py
|       |       |
|       |       +---commands  <-- Менеджмент команда для заполнения Модели "Ингредиенты"
|       |               import_csv_data.py
|       |
|       +---static
|       |
|       \---users
|           |   admin.py
|           |   apps.py
|           |   forms.py
|           |   managers.py
|           |   models.py
|           |   validators.py
|           |   __init__.py
|           |
|           +---migrations
|
+---data  <-- Данные для наполнения БД "Ингредиенты"
|       fixtures.json.gz
|       ingredients.csv
|       media_recipes.tar
|
+---docs  <-- Документация по API
|       openapi-schema.yml
|       redoc.html
|
+---frontend  <-- Фронтенд для сборки файлов
|   |   Dockerfile
|   ...
|         
+---infra  <-- Сборка контейнеров, настройка сервера
|       docker-compose.yml
|       nginx.conf
|       
\---venv
|   ...
```

- Склонируйте репозиторий на свой компьютер:

```py
https://github.com/nvtaranets/foodgram-project-react/
```

- Соберите контейнеры из папки `infra`:

```py
docker-compose up -d
```

- В контейнере **backend**:
    - выполните миграции;
    - соберите статику проекта  
    - установите **superuser**;
    - заполните БД исходными данными:

```py
docker-compose exec backend python manage.py migrate users
docker-compose exec backend python manage.py migrate --fake-initial --run-syncdb
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend bash
python manage.py createsuperuser
.
.
.
exit
docker-compose exec backend python manage.py imort_csv_data ingredients.csv
```

[⬆️Оглавление](#оглавление)

</details>

## Автор

[Николай Таранец](https://github.com/nvtaranets)  


[![Foodgram CI/CD](https://github.com/NVTaranets/foodgram-project-react/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/NVTaranets/foodgram-project-react/actions/workflows/ci-cd.yml)