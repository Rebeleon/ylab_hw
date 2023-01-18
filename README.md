1. Создать виртуальное окружение командой python3 -m venv имя_окружения
2. Активировать его source имя_окружения/bin/activate
3. Установить зависимости в виртуальное окружение python -m pip install -r requirements.txt или pip install -r requirements.txt
4. В файле .env заполнить данные для подключения к БД Postgres
5. Создать таблицы в БД. В проекте использовался Alembic для создания миграций и таблиц в БД. Можно воспользоваться им же
https://alembic.sqlalchemy.org/en/latest/.
6. Для запуска проекта на локальном сервере используется команда uvicorn main:app --reload
