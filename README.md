### О проекте

Проект приложения для Благотворительного фонда поддержки котиков QRKot.

### Технологический стек

Python 3.9

SQLAlchemy 1.4.36

Alembic 1.7.7

Fastapi 0.78.0

Fastapi-users 10.0.4

Pydantic 1.9.1

### Автор

Никита Сергеевич Федяев

Telegram: [@nsfed](https://t.me/nsfed)

Репозиторий: [GitHub](git@github.com:Fedoska48/cat_charity_fund.git)

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Fedoska48/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Предварительно перед запуском необходимо запонить файл .env:

APP_TITLE=QRKot

APP_DESCRIPTION=Кошачий благотворительный фонд

DATABASE_URL=sqlite+aiosqlite:///./qrkot.db

SECRET=Secret

FIRST_SUPERUSER_EMAIL=superuser@superuser.com

FIRST_SUPERUSER_PASSWORD=superuser

* Создать файл миграций:

```
alembic revision --autogenerate -m "Init migration"
```

* Выполнить миграции:

```
alembic upgrade head
```

* Запустить проект можно командой в терминале:

```
uvicorn app.main:app --reload
```
При первом запуске автоматически создается "Суперюзер" с параметрами 
FIRST_SUPERUSER_EMAIL, FIRST_SUPERUSER_PASSWORD из .env - файла

### Описание API:

**/redoc** — документация в формате **ReDoc**;


**/docs** — документация в формате **Swagger**
