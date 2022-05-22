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
|   .env
|   .gitignore
|   README.md
|   
+---backend  <--
|   |   Dockerfile
|   |   manage.py
|   |   requirements.txt
|   |   
|   +---api
|   |   |   apps.py
|   |   |   filters.py
|   |   |   pagination.py
|   |   |   permissions.py
|   |   |   urls.py
|   |   |   utils.py
|   |   |   views.py
|   |   |   __init__.py
|   |   |   
|   |   \---__pycache__
|   |           
|   +---backend
|   |   |   asgi.py
|   |   |   settings.py
|   |   |   urls.py
|   |   |   wsgi.py
|   |   |   __init__.py
|   |   |   
|   |   \---__pycache__
|   |           
|   +---data  <-- Данные для наполнения БД "Ингредиенты"
|   |       ingredients.csv
|   |       ingredients.json
|   |       
|   +---recipes
|   |   |   admin.py
|   |   |   apps.py
|   |   |   models.py
|   |   |   serializers.py
|   |   |   views.py
|   |   |   __init__.py
|   |   |           
|   |   \---__pycache__
|   |           
|   +---scripts  <-- Скрипт для заполнения БД "Ингредиенты"
|   |   |   load_ing_data.py
|   |   |   __init__.py
|   |   |   
|   |   \---__pycache__
|   |           
|   \---users
|       |   admin.py
|       |   apps.py
|       |   models.py
|       |   serializers.py
|       |   views.py
|       |   __init__.py
|       |   
|       \---__pycache__
|               
+---docs  <-- Документация по API
|       openapi-schema.yml
|       redoc.html
|       
+---frontend  <-- Фронтенд для сборки файлов
|   |   Dockerfile
|   |   package-lock.json
|   |   package.json
|   |   yarn.lock
|   |   
|   ...
|         
+---infra  <-- Сборка контейнеров, настройка сервера
|       docker-compose.yml
|       nginx.conf
|       
\---venv
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
    - установите **superuser**;
    - заполните БД исходными данными:

```py
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py runscript load_ing_data
```

[⬆️Оглавление](#оглавление)

</details>

## Автор

[Николай Таранец](https://github.com/nvtaranets)  


[![Foodgram CI/CD](https://github.com/NVTaranets/foodgram-project-react/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/NVTaranets/foodgram-project-react/actions/workflows/ci-cd.yml)