## Задание 5 Задание 6

В некотором смылсе модификация задания 4. Однако теперь вместо парсера - Docker. Эта программа разделяет всю свою логику между двумя Docker контейнерами: в первом лежит бд, во втором - обработчик запросов

## Запуск

Контейнер с бд:
````
docker run -d --name db --network my_network -e POSTGRES_DB=avito_parser -e POSTGRES_USER=parser_user -e POSTGRES_PASSWORD=password postgres
````

Контейнер приложения (внимание, делать в той же папке, где лежит dockerfile):
````
docker build -t my_fastapi_app .
docker run -d --name app --network my_network -p 5000:5000 my_fastapi_app
````

Теперь, если всё сделано правильно, вам должен быть доступен: http://localhost:5000/docs

Для задания 6:
Необходимо создать контейнер с nginx:
````
docker run -d --name nginx_proxy --network my_network -p 80:80 -v "Абсолютный путь к файлу nginx.conf:/etc/nginx/nginx.conf:ro" nginx
````
Внимание! следите за названиями сети my_network, все трое должны быть в одной сети, иначе ничего работать не будет!
Теперь, если всё правильно, свагер вам будет доступен по адресу: http://localhost/docs

## Использование
Запрос на добавление url в базу данных:
````
curl -X POST "http://localhost:5000/parse?url=YOUR_URL" -H "accept: application/json"
````
Ожидаемый ответ: {"message":"URL added successfully"}

Запрос на показ всех добавленных url:
````
curl -X GET "http://localhost:5000/ads" -H "accept: application/json"
````
Ожидаемый ответ: {"id":1,"link":"https://vk.com/feed"},...

## Использование задание 6
Запрос на добавление url в базу данных:
````
curl -X POST "http://localhost/parse?url=YOUR_URL" -H "accept: application/json"
````
Ожидаемый ответ: {"message":"URL added successfully"}

Запрос на показ всех добавленных url:
````
curl -X GET "http://localhost/ads" -H "accept: application/json"
````
Ожидаемый ответ: {"id":1,"link":"https://vk.com/feed"},...
