## Задание 4

Данная программа с помощью Selenium парсит первые пять странци с объявлениями Avito (Открыть авито, забить какой-то определённый запрос, например игровые ноутбуки, скопировать ссылку на эту страницу), загружает результ в бд на PostgreSQL, позволяет по определённому запросу получить данные из БД

## Перед запуском

В первую очередь необходимо настроить БД
1. Заходим в терминал и запускаем команду:
````
psql -U postgres
````
2. Создаём бд:
````
CREATE DATABASE avito_parser;
````
3. Создаём пользователя:
````
CREATE USER parser_user WITH PASSWORD 'password';
````
!Обратите внимание ваш password должен совпадать с таковым в database.py в переменной SQLALCHEMY_DATABASE_URL!

4. Даём пользователю права пользование БД:
````
GRANT ALL PRIVILEGES ON DATABASE avito_parser TO parser_user;
````

Если в дальнейшем возникает ошибка доступа, необходимо дополнительно настроить разрешения:

Подключаемся к бд:
````
psql -U postgres -d avito_parser
````

Даём все необходимые права:
````
GRANT USAGE ON SCHEMA public TO parser_user;
GRANT CREATE ON SCHEMA public TO parser_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO parser_user;
ALTER SCHEMA public OWNER TO parser_user;
````
5. Выходим из psql:
````
\q
````

## Запуск

1. В папке с программой выполняем команду, она запустит сервер:
````
uvicorn main:app --reload
````
2. Чтобы проверить доступные методы можно открыть в браузере интерфейс Swagger, просто вводим в поисковую строку:
````
http://localhost:8000/docs
````
3. В новом терминале выполняем команду, она запустит парсинг:
````
curl "http://localhost:8000/parse?url=your_url"
````
Обратите внимание, необходимо указать url конкретной страницы (см. самое начало readme).
Парсинг занимает примерно 1-2 минуты

4. Выполняем команду:
````
curl http://localhost:8000/ads
````
Она вернёт результаты парсинга

